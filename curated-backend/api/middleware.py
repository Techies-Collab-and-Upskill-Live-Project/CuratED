import logging
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)

class APIErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
            return JsonResponse(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
