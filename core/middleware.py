# middleware.py
from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve

class APIKeyMiddleware:
    """
    Middleware to check for a valid API key in the request headers for API endpoints.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for API key for requests that start with /api/
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-KEY')
            
            if api_key != settings.API_KEY:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

        # Proceed with the request
        return self.get_response(request)