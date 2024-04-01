import logging

logger = logging.getLogger(__name__)

class UserActionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log the user's action, username, and request path
        if request.user.is_authenticated:
            action_message = f"User '{request.user.username}' accessed '{request.path}'"
            logger.info(action_message)

        return response
