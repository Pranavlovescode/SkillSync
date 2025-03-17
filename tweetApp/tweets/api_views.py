from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, SkillPost
from .serializers import UserSerializer, SkillPostSerializer

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
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
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
        post = self.get_object()
        post.post_likes += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        posts = SkillPost.objects.filter(post_owner=request.user).order_by('-createdAt')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data) 