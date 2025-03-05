import logging
import time
from django.utils.timezone import localtime
from pdb import set_trace

logger = logging.getLogger('django')

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Log request details
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.get_full_path()}")

        # Log the request body if needed (be careful with sensitive data)
        if request.body:
            logger.debug(f"Request Body: {request.body.decode('utf-8')}")

        response = self.get_response(request)

        # Log response details
        elapsed_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} in {elapsed_time:.2f} seconds")

        # Log the response body if needed (be careful with sensitive data)
        if hasattr(response, 'content'):
            logger.debug(f"Response Body: {response.content.decode('utf-8')}")

        return response
