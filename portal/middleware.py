from django.conf import settings
from django.shortcuts import render


class NoCacheMiddleware:
    """
    Prevents browsers from caching sensitive administrative, student, and staff dashboard pages.
    Defeats back-button history navigation after logout.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Apply strict anti-caching headers for authenticated sessions and dashboard routes
        if request.user.is_authenticated or request.path.startswith('/portal/') or request.path.startswith('/admin/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response


class MaintenanceModeMiddleware:
    """
    Displays a maintenance page to all public visitors when MAINTENANCE_MODE=True.

    Bypass rules (always allowed through):
      - Django admin  → /admin/*
      - Staff portal  → /portal/login/, /portal/register/
      - Authenticated superusers / staff users
      - Static & media assets  → /static/*, /media/*
    """

    # Paths that are never blocked, even during maintenance
    ALLOWED_PATHS = [
        '/admin/',
        '/portal/login/',
        '/portal/register/',
        '/login/',
        '/static/',
        '/media/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        maintenance = getattr(settings, 'MAINTENANCE_MODE', False)

        if maintenance:
            # Always let staff / superusers through
            user = getattr(request, 'user', None)
            if user and user.is_authenticated and (user.is_staff or user.is_superuser):
                return self.get_response(request)

            # Always let whitelisted paths through
            for path in self.ALLOWED_PATHS:
                if request.path.startswith(path):
                    return self.get_response(request)

            # Serve the maintenance page with HTTP 503
            return render(request, 'maintenance.html', status=503)

        return self.get_response(request)
