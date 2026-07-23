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
