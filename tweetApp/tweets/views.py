from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from tweets.models import User
from .serializers import UserSerializer

# Create your views here.

@csrf_exempt
def list_users(request):
    """
    List all users or create a new one 
    """
    if request.method == 'GET':
        users = User.objects.all()
        response = UserSerializer(users,many=True)
        return JsonResponse(response.data,safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    

@csrf_exempt
def update_or_delete_or_get_user_details(request,email):

# Trying to find the user from provided user_id
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message":"Failed to find the user"},status=400)
    
    if request.method == 'GET':
        foundUser = UserSerializer(user)
        return JsonResponse(foundUser.data,status=200)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        updatedUser = UserSerializer(user,data=data)
        if updatedUser.is_valid():
            updatedUser.save()
            return JsonResponse(updatedUser.data)
        else:
            return JsonResponse(updatedUser.errors,status=400)
        

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({"message":"User deleted successfully"},status=204)


