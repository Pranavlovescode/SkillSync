from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from tweets.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        try:
            # Try to get the user by email or username
            user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()
            print(f"Found user: {user}")
            
            # Log the password and check the comparison
            if check_password(password,user.password):
                print("Password matches")
                return user
            else:
                print("Password does not match")
        except User.DoesNotExist:
            print(f"No user found with username: {username_or_email}")
            return None
