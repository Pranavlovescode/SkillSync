from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','name','email','phone_number','password','dob','profile_photo','gender']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def validate_password(self, value):
        # Add any custom password validation here if needed
        return value