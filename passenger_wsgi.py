import os
import sys

# Add project root directory to Python path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Point to Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctrla_hub.settings')

# Expose WSGI application for Phusion Passenger / cPanel Python App
from ctrla_hub.wsgi import application
wsgi = application
