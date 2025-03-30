from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User, SkillPost, SkillCategory, Skill, SkillEndorsement
from .serializers import (
    UserSerializer, SkillPostSerializer, 
    SkillCategorySerializer, SkillSerializer, 
    SkillEndorsementSerializer, SkillCategoryWithSkillsSerializer
)
from rest_framework.authentication import SessionAuthentication,BaseAuthentication

# Traditional view functions
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ProfileForm
import json



@api_view(['GET'])
def tweet_view(request):
    """
    View for displaying tweets/skills as JSON
    """
    posts = SkillPost.objects.all().order_by('-createdAt')
    serializer = SkillPostSerializer(posts, many=True)
    
    user_email = request.session.get('user')
    is_authenticated = user_email is not None
    
    return JsonResponse({
        'pageTitle': 'Skills Feed',
        'isAuthenticated': is_authenticated,
        'posts': serializer.data
    })

@api_view(['GET','POST'])
def profile_view(request):
    """
    View for displaying user profile as JSON
    """
    user_email = request.session.get('user')
    if not user_email:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    
    user = User.objects.get(email=user_email)
    posts = SkillPost.objects.filter(post_owner=user).order_by('-createdAt')
    
    user_serializer = UserSerializer(user)
    posts_serializer = SkillPostSerializer(posts, many=True)
    
    return JsonResponse({
        'pageTitle': f"{user.first_name}'s Profile",
        'isAuthenticated': True,
        'user': user_serializer.data,
        'posts': posts_serializer.data
    })

@api_view(['POST'])
def edit_profile_view(request):
    """
    View for editing user profile with JSON responses
    """
    user_email = request.session.get('user')
    if not user_email:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    
    user = User.objects.get(email=user_email)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Update user fields
            for field, value in data.items():
                if hasattr(user, field) and field not in ['user_id', 'password', 'createdAt']:
                    setattr(user, field, value)
            
            user.save()
            serializer = UserSerializer(user)
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    # For GET requests, return user data
    serializer = UserSerializer(user)
    return JsonResponse({
        'pageTitle': 'Edit Profile',
        'isAuthenticated': True,
        'user': serializer.data
    })

@api_view(['POST'])
def create_new_post(request):
    """
    View for creating a new skill post with JSON responses
    """
    user_email = request.session.get('user')
    if not user_email:
        print("user_email",user_email)
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    
    user = User.objects.get(email=user_email)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_name = data.get('post_name')
            post_description = data.get('post_description')
            post_tags = data.get('post_tags')
            
            # Validate required fields
            if not all([post_name, post_description]):
                return JsonResponse({
                    'success': False,
                    'error': 'Post name and description are required'
                }, status=400)
            
            post = SkillPost(
                post_name=post_name,
                post_description=post_description,
                post_tags=post_tags,
                post_owner=user
            )
            
            # Handle media separately if needed
            # This would require additional frontend handling for file uploads
            
            post.save()
            serializer = SkillPostSerializer(post)
            
            return JsonResponse({
                'success': True,
                'message': 'Post created successfully',
                'post': serializer.data,
                'redirect': '/skill/'
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    # For GET requests, return form initial state
    return JsonResponse({
        'pageTitle': 'Create New Post',
        'isAuthenticated': True
    })

@api_view(['POST'])
def create_new_skills(request):
    """
    View for creating a new skill post with JSON responses
    """
    user_email = request.session.get('user')
    if not user_email:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    
    user = User.objects.get(email=user_email)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_name = data.get('post_name')
            post_description = data.get('post_description')
            post_level = data.get('post_level', 'Beginner')  # Default to 'Beginner' if not provided
            post_tags = data.get('post_tags')
            
            # Validate required fields
            if not all([post_name, post_description]):
                return JsonResponse({
                    'success': False,
                    'error': 'Post name and description are required'
                }, status=400)
                
            # Validate level field
            if not post_level or post_level not in [choice[0] for choice in Skill.LEVEL_CHOICES]:
                post_level = 'Beginner'  # Default to Beginner if invalid
            
            # Validate category exists
            if not post_tags:
                return JsonResponse({
                    'success': False,
                    'error': 'Category is required'
                }, status=400)
                
            try:
                category = SkillCategory.objects.get(id=post_tags)
            except SkillCategory.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid category'
                }, status=400)
            
            post = Skill(
                name=post_name,
                description=post_description,
                level=post_level,
                category=category,
                user=user
            )
            
            post.save()
            serializer = SkillSerializer(post)
            
            return JsonResponse({
                'success': True,
                'message': 'Skill created successfully',
                'post': serializer.data,
                'redirect': '/skill/'
            }, status=201)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    # For GET requests, return form initial state
    return JsonResponse({
        'pageTitle': 'Create New Post',
        'isAuthenticated': True
    })



@api_view(['GET'])
def get_user_skills(request, username):
    """
    Get all skills for a specific user
    """
    user = get_object_or_404(User, username=username)
    skills = Skill.objects.filter(user=user)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_skill_categories_with_skills(request):
    """
    Get all skill categories with their related skills
    """
    categories = SkillCategory.objects.all()
    serializer = SkillCategoryWithSkillsSerializer(categories, many=True)
    return Response(serializer.data) 


@api_view(['POST','GET'])
def add_category(request):
    """
    Add a new category
    """
    user_email = request.session.get('user')
    if not user_email:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    
    if request.method == 'POST' and user_email:
        if not user_email:
            return JsonResponse({
                'success': False,
                'error': 'Not authenticated',
                'redirect': '/'
            }, status=401)
        data = json.loads(request.body)
        serializer = SkillCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET' and user_email:
        categories = SkillCategory.objects.all()
        serializer = SkillCategorySerializer(categories, many=True)
        return Response(serializer.data)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['GET'])
def get_skill_by_category(request,category_id):
    """
    Get all skills for a specific category
    """
    user_email = request.session.get('user')
    if not category_id:
        return JsonResponse({
            'success': False,
            'error': 'Category ID is required',
            'redirect': '/'
        }, status=400)
    if not user_email:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated',
            'redirect': '/'
        }, status=401)
    try:
        category = SkillCategory.objects.get(id=category_id)
        skills = Skill.objects.filter(category=category)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
    except SkillCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)