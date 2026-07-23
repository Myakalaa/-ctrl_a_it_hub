import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrla_hub.settings')
django.setup()

from django.template.loader import render_to_string
from portal.models import Course
from django.test import RequestFactory

rf = RequestFactory()
request = rf.get('/courses/')

courses = Course.objects.all()
categories = Course.CATEGORY_CHOICES
context = {
    'courses': courses,
    'categories': categories,
    'query': '',
    'selected_category': '',
}

try:
    html = render_to_string('courses.html', context, request=request)
    print('Template rendered successfully!')
    print('Rendered course count:', html.count('class=\"course-card\"') + html.count('class=\'course-card\''))
except Exception as e:
    print('Error rendering template:', e)
