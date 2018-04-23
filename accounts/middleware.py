from .models import User
from django.contrib.auth import authenticate
from django.utils import timezone

class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated():
            request.user.last_visit = timezone.now()
            request.user.save(update_fields=['last_visit'])
        # Update last visit time before request finished processing.
        response = self.get_response(request)
        # Update last visit time after request finished processing.
        return response
