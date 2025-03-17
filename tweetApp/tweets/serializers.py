from rest_framework import serializers
from .models import User, SkillPost, SkillCategory, Skill, SkillEndorsement
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

class SkillCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for SkillCategory model
    """
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'description', 'icon', 'created_at']

class SkillEndorsementSerializer(serializers.ModelSerializer):
    """
    Serializer for SkillEndorsement model
    """
    endorsed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SkillEndorsement
        fields = ['id', 'endorsed_by', 'created_at']

class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for Skill model
    """
    category = SkillCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SkillCategory.objects.all(),
        source='category',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    endorsements_count = serializers.SerializerMethodField()
    endorsements = SkillEndorsementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'level', 
            'category', 'category_id', 'user', 
            'created_at', 'endorsements_count', 'endorsements'
        ]
    
    def get_endorsements_count(self, obj):
        return obj.endorsements.count()

class SkillCategoryWithSkillsSerializer(serializers.ModelSerializer):
    """
    Serializer for SkillCategory model with related skills
    """
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'description', 'icon', 'created_at', 'skills']