from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from tweets.models import User
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as DjangoUser
import logging

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        logger.debug(f"Attempting to authenticate with username/email: {username_or_email}")
        
        try:
            # Try to get the user by email
            user_by_email = User.objects.filter(email=username_or_email).first()
            if user_by_email:
                logger.debug(f"Found user by email: {user_by_email.email}")
                user = user_by_email
            else:
                # Try to get the user by username
                user_by_username = User.objects.filter(username=username_or_email).first()
                if user_by_username:
                    logger.debug(f"Found user by username: {user_by_username.username}")
                    user = user_by_username
                else:
                    logger.debug(f"No user found with email or username: {username_or_email}")
                    return None
            
            # Debug password check
            logger.debug(f"Checking password for user: {user.username}")
            password_valid = check_password(password, user.password)
            logger.debug(f"Password valid: {password_valid}")
            
            if password_valid:
                return user
            return None
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CustomTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication for non-Django User model
    """
    def authenticate(self, request):
        # First, use the parent class to authenticate with Django User
        auth_result = super().authenticate(request)
        
        if auth_result is None:
            return None
            
        django_user, token = auth_result
        
        # Map the Django User to our custom User model
        try:
            custom_user = User.objects.get(username=django_user.username)
            return (custom_user, token)
        except User.DoesNotExist:
            # If no matching custom user exists, try to create one
            try:
                custom_user = User.objects.get(email=django_user.email)
                return (custom_user, token)
            except User.DoesNotExist:
                # No matching user found
                raise AuthenticationFailed('User not found in custom User model')

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # Get the Django User
        django_user = token.user
        
        # Map to custom User
        try:
            custom_user = User.objects.get(username=django_user.username)
            return (custom_user, token)
        except User.DoesNotExist:
            try:
                custom_user = User.objects.get(email=django_user.email)
                return (custom_user, token)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found in custom User model')
