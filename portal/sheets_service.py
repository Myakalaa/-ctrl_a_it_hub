import os
import datetime
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

SPREADSHEET_ID = '1oeXanGjhXfwzMLVINx-aZjDt78sVJPE8THngeEEl5bI'

def append_lead_to_google_sheet(student_name: str, phone: str, course: str = "General IT Training", email: str = "") -> bool:
    """
    Directly appends student lead details into Google Sheets ('Lead Sheet')
    using Google Service Account credentials.
    100% Free Forever without n8n.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        creds_path = os.path.join(settings.BASE_DIR, 'google_credentials.json')
        if not os.path.exists(creds_path):
            logger.warning(f"[Sheets Service] Credentials not found at {creds_path}")
            return False

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(credentials)

        sheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.get_worksheet(0)  # First sheet: Sheet1

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Row format matches your sheet headers: Name, Phone, Course, Date
        row = [student_name, phone, course or "IT Training Programs", now_str]
        worksheet.append_row(row)

        logger.info(f"[Sheets Service] ✓ Successfully appended lead for '{student_name}' to Google Sheet.")
        return True

    except Exception as e:
        logger.warning(f"[Sheets Service] Could not append lead to Google Sheet: {e}")
        return False
