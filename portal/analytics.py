import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from django.conf import settings
from django.core.cache import cache

def get_visitor_stats():
    """
    Fetches the last 7 days of daily active users from Google Analytics 4.
    Caches the result for 15 minutes to save API quotas.
    """
    cached_data = cache.get('ga_visitor_stats')
    if cached_data:
        return cached_data

    # 1. Authenticate with the JSON Key
    creds_path = os.path.join(settings.BASE_DIR, 'google_credentials.json')
    if not os.path.exists(creds_path):
        return {'dates': [], 'visitors': []}

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
    
    # 2. Get Property ID (Needs to be added to .env)
    property_id = getattr(settings, 'GA_PROPERTY_ID', None)
    if not property_id:
        # Fallback dummy data if ID is missing so dashboard still renders
        return {'dates': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'visitors': [10, 25, 40, 15, 60, 45, 80]}

    # 3. Query Google Analytics
    try:
        client = BetaAnalyticsDataClient()
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )
        response = client.run_report(request)

        dates = []
        visitors = []
        for row in response.rows:
            date_str = row.dimension_values[0].value
            # Format YYYYMMDD to MM/DD
            formatted_date = f"{date_str[4:6]}/{date_str[6:8]}"
            dates.append(formatted_date)
            visitors.append(int(row.metric_values[0].value))

        data = {'dates': dates, 'visitors': visitors}
        cache.set('ga_visitor_stats', data, 60 * 15)  # Cache for 15 mins
        return data
    except Exception as e:
        print(f"GA Data API Error: {e}")
        # Return empty data on failure so dashboard doesn't crash
        return {'dates': [], 'visitors': []}
