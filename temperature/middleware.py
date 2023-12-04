import os
from django.http import JsonResponse

class TokenCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.app_token = os.environ.get('TEMPERATURE_APP_TOKEN')

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        provided_token = auth_header.split(' ')[1]
        if provided_token != self.app_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        response = self.get_response(request)
        return response
