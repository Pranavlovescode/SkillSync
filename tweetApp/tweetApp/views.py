import cloudinary.uploader
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate
from tweets.models import User
from tweets.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,os
from django.contrib.auth.models import User as DjangoUser
import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)



cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("CLOUD_API_KEY"),
    api_secret = os.getenv("CLOUD_API_SECRET")
)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def login_api(request):
    """
    API endpoint for user login using DRF's authentication
    """
    # Handle GET requests
    if request.method == 'GET':
        return Response({
            'message': 'Please provide username and password to login',
            'isAuthenticated': request.user.is_authenticated if hasattr(request, 'user') else False
        })
    
    # Handle POST requests
    username = request.data.get('username_or_email')
    password = request.data.get('password')
    
    print(f'Login attempt for: {username}')
    
    if not username or not password:
        return Response(
            {'message': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Use Django's built-in authentication
    django_user = authenticate(username=username, password=password)
    
    if not django_user:
        # Try with email
        try:
            django_user_obj = DjangoUser.objects.get(email=username)
            django_user = authenticate(username=django_user_obj.username, password=password)
        except DjangoUser.DoesNotExist:
            return Response(
                {'message': 'User does not exist'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    if django_user:
        # Get or create token
        # token, created = Token.objects.get_or_create(user=django_user)
        
        # Get or create custom user
        try:
            custom_user = User.objects.get(username=django_user.username)
        except User.DoesNotExist:
            # Return the message that the user does not exist
            return Response(
                {'message': 'User does not exist'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Store in session
        # request.session['auth_token'] = token.key
        request.session['user'] = custom_user.email
        
        serializer = UserSerializer(custom_user)
        return Response({
            'message': 'Login successful',
            # 'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'message': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    """
    API endpoint for user registration
    """
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate required fields
    if not all([first_name, last_name, email, username, password]):
        return Response(
            {'message': 'All fields are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user already exists in Django User model
    if DjangoUser.objects.filter(email=email).exists():
        return Response(
            {'message': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if DjangoUser.objects.filter(username=username).exists():
        return Response(
            {'message': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create Django User first (this is the primary user for authentication)
    # Define a default profile image relative to your media directory

    # Upload default profile image
# Upload default profile image
    # try:
    #     image_path = os.path.join('media', 'user.jpg')  
    #     cloudinary_response = cloudinary.uploader.upload(
    #         image_path, 
    #         folder='SkillSync/profile_photo',
    #         resource_type='image'
    #     )
    #     profile_photo_url = cloudinary_response.get('secure_url')
    # except Exception as e:
    #     print(f"Cloudinary upload error: {str(e)}")
    #     profile_photo_url = None  # Use None if upload fails

    # Upload the default image to Cloudinary
    # image_path = os.path.join('media', 'user.jpg')
    # upload_result = cloudinary.uploader.upload(image_path, folder="SkillSync/profile_photo")

    # Get the secure URL from Cloudinary response
    # secure_url = upload_result.get("secure_url")
    default_image_path = 'https://res.cloudinary.com/dwsjntvgq/image/upload/v1743408181/SkillSync/profile_photo/s4qbhsl5b1uqshpmyua1.jpg'
    django_user = DjangoUser.objects.create_user(
        username=username,
        email=email,
        password=password,  # This will be hashed by create_user
        first_name=first_name,
        last_name=last_name,
        
    )
    
    
    # Create custom User with the same data
    hash_password = django_user.password  # Already hashed by Django
    
        
    custom_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hash_password,
            profile_photo=default_image_path,  # Use the secure URL from Cloudinary
        )
    
    
    # Create token for the Django User
    token, created = Token.objects.get_or_create(user=django_user)
    
    # Store the token in the session for future use
    request.session['auth_token'] = token.key
    request.session['user'] = custom_user.email
    
    serializer = UserSerializer(custom_user)
    return Response({
        'message': 'Signup successful',
        'token': token.key,
        'user': serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST','GET'])
@permission_classes([AllowAny])
def logout_api(request):
    """
    API endpoint for user logout
    """
    try:
        # # Get the token from either the Authorization header or session
        # auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        # token_key = None
        
        # if auth_header.startswith('Token '):
        #     token_key = auth_header.split(' ')[1]
        # else:
        #     token_key = request.session.get('auth_token')
        
        # if token_key:
        #     try:
        #         # Delete the token
        #         token = Token.objects.get(key=token_key)
        #         token.delete()
        #     except Token.DoesNotExist:
        #         pass  # Token might already be deleted
        user_email = request.session.get('user')
        if not user_email:
            return Response(
                {'message': 'User not logged in'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Clear session
        request.session.flush()
        
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response(
            {'message': 'Error during logout'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Legacy views modified to provide JSON responses for React frontend
# @csrf_exempt
# def login_view(request):
#     """
#     Login view that returns initial state for React
#     """
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username_or_email = data.get('username_or_email')
#         password = data.get('password')
        
#         custom_backend = EmailBackend()
#         user = custom_backend.authenticate(
#             request=request,
#             username_or_email=username_or_email,
#             password=password
#         )
        
#         if user:
#             request.session['user'] = user.email
#             serializer = UserSerializer(user)
#             return JsonResponse({
#                 'success': True,
#                 'user': serializer.data,
#                 'redirect': '/skill/'
#             })
#         else:
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Invalid credentials'
#             }, status=401)
    
#     # For GET requests, return initial state
#     return JsonResponse({
#         'pageTitle': 'Login',
#         'isAuthenticated': 'user' in request.session
#     })

# def signup_view(request):
#     """
#     Signup view that returns initial state for React
#     """
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         email = data.get('email')
#         username = data.get('username')
#         password = data.get('password')
        
#         # Validate required fields
#         if not all([first_name, last_name, email, username, password]):
#             return JsonResponse({
#                 'success': False,
#                 'error': 'All fields are required'
#             }, status=400)
        
#         # Check if user already exists
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Email already registered'
#             }, status=400)
        
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({
#                 'success': False,
#                 'error': 'Username already taken'
#             }, status=400)
        
#         # Create user
#         hash_password = make_password(password)
#         user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             username=username,
#             password=hash_password
#         )
#         user.save()
        
#         # Set session
#         request.session['user'] = user.email
#         serializer = UserSerializer(user)
#         return JsonResponse({
#             'success': True,
#             'user': serializer.data,
#             'redirect': '/skill/'
#         }, status=201)
    
#     # For GET requests, return initial state
#     return JsonResponse({
#         'pageTitle': 'Sign Up',
#         'isAuthenticated': 'user' in request.session
#     })

# def logout_view(request):
#     """
#     Logout view that clears session and returns success response
#     """
#     if 'user' in request.session:
#         request.session.flush()
    
#     return JsonResponse({
#         'success': True,
#         'message': 'Successfully logged out',
#         'redirect': '/'
#     })