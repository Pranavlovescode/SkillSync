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

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.post_owner.user_id == request.user.user_id

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally restricts the returned users,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's profile
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """
        Update the current user's profile
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for skill posts
    """
    queryset = SkillPost.objects.all().order_by('-createdAt')
    serializer_class = SkillPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(post_owner=self.request.user)
    
    def get_queryset(self):
        """
        Optionally filter posts by tag or user
        """
        queryset = SkillPost.objects.all().order_by('-createdAt')
        tag = self.request.query_params.get('tag', None)
        user_id = self.request.query_params.get('user_id', None)
        
        if tag is not None:
            queryset = queryset.filter(post_tags__icontains=tag)
        
        if user_id is not None:
            queryset = queryset.filter(post_owner__user_id=user_id)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        Like a post
        """
        post = self.get_object()
        post.post_likes += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Get posts created by the current user
        """
        posts = SkillPost.objects.filter(post_owner=request.user).order_by('-createdAt')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

# Views modified to provide JSON responses for React frontend
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
@permission_classes([IsAuthenticated])
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
            category_id = request.GET.get('category_id')
            
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
            if not category_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Category is required'
                }, status=400)
                
            try:
                category = SkillCategory.objects.get(id=category_id)
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


# Skill Category ViewSet
class SkillCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for skill categories
    """
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return SkillCategoryWithSkillsSerializer
        return SkillCategorySerializer


# Skill ViewSet
class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for skills
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Skill.objects.all()
        
        # Filter by category if provided
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by user if provided
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by level if provided
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        return queryset
    
    def perform_create(self, serializer):
        # Set the user to the current authenticated user
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def endorse(self, request, pk=None):
        """
        Endpoint for endorsing a skill
        """
        skill = self.get_object()
        user = request.user
        
        # Check if the user has already endorsed this skill
        if SkillEndorsement.objects.filter(skill=skill, endorsed_by=user).exists():
            return Response(
                {'detail': 'You have already endorsed this skill.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the endorsement
        endorsement = SkillEndorsement.objects.create(
            skill=skill,
            endorsed_by=user
        )
        
        serializer = SkillEndorsementSerializer(endorsement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_skills(request, username):
    """
    Get all skills for a specific user
    """
    user = get_object_or_404(User, username=username)
    skills = Skill.objects.filter(user=user)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_skill_categories_with_skills(request):
    """
    Get all skill categories with their related skills
    """
    categories = SkillCategory.objects.all()
    serializer = SkillCategoryWithSkillsSerializer(categories, many=True)
    return Response(serializer.data) 