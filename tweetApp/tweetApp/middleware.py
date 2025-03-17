from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from tweets.models import User
from django.contrib.auth.models import User as DjangoUser
import logging

logger = logging.getLogger(__name__)

class CustomMiddleware:

    # One time initialisation
    def __init__(self, get_response):
        self.get_response = get_response

    # Code to be executed for each request before the view is called
    def __call__(self, request):
        logger.debug("Middleware executed")
        
        # URLs that don't require authentication
        open_urls = ['/', '/signup/']
        
        # Skip middleware for all API endpoints
        if request.path.startswith('/api/'):
            return self.get_response(request)
            
        # Check for session-based authentication
        session_user = request.session.get('user')
        
        # Check for token-based authentication in headers
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_auth = False
        
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                # Get the Django user
                django_user = token.user
                
                # Set session user if token is valid
                if not session_user:
                    try:
                        # Try to find corresponding custom user
                        custom_user = User.objects.get(username=django_user.username)
                        request.session['user'] = custom_user.email
                        session_user = custom_user.email
                    except User.DoesNotExist:
                        logger.warning(f"No custom user found for Django user: {django_user.username}")
                
                token_auth = True
            except Token.DoesNotExist:
                logger.warning(f"Invalid token: {token_key}")
                
        # Redirect to login if not authenticated and not on an open URL
        if request.path not in open_urls and not (session_user or token_auth):
            logger.debug("Redirecting to login page")
            return HttpResponseRedirect('/')
            
        # Redirect to main page if authenticated and on an open URL
        elif request.path in open_urls and (session_user or token_auth):
            logger.debug("Redirecting to tweet page")
            return HttpResponseRedirect('/skill/')
            
        response = self.get_response(request)
        return response