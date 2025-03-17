from rest_framework import serializers
from .models import User, SkillPost
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 
            'username', 'phone_number', 'password', 'dob', 
            'profile_photo', 'gender', 'bio', 'createdAt'
        ]
        read_only_fields = ['user_id', 'createdAt']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Handle password updates properly
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def validate_password(self, value):
        # Add any custom password validation here if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

class SkillPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillPost
        fields = [
            'post_id', 'post_name', 'post_description', 
            'post_media', 'post_tags', 'post_owner', 
            'post_likes', 'createdAt'
        ]
        read_only_fields = ['post_id', 'createdAt']