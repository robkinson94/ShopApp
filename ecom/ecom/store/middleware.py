# myapp/middleware.py
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings

class InactivityTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the last activity time from the session
        last_activity_str = request.session.get('last_activity')

        # Convert last_activity string to datetime object
        last_activity = timezone.datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S.%f%z') if last_activity_str else None

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # If last_activity is not set, or the user has been inactive for SESSION_COOKIE_AGE seconds
            if not last_activity or (timezone.now() - last_activity).total_seconds() > settings.SESSION_COOKIE_AGE:
                logout(request)  # Log out the user

        # Update last activity time in the session as a string
        request.session['last_activity'] = str(timezone.now())

        # Continue processing the request
        response = self.get_response(request)
        return response


