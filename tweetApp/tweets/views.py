
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from tweets.models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

# Create your views here.

# Initial routes(login,register,logout)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        serialzer  = UserSerializer(user)
        print('user',serialzer.data)
        if check_password(password, user.password):
            request.session['user_id'] = user.email
            return Response({'message': 'Login successful',"user":serialzer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

    


@api_view(['GET'])
def logout_view(request):
    request.session.flush()  # clear the session
    return JsonResponse({"msg":"Logout successful"},status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def register_view(request):
    try:
        data = JSONParser().parse(request)
        # print("Data received:", data)

        serializer = UserSerializer(data=data)
        # print("Serializer initialized:", serializer)

        if serializer.is_valid():
            # print("Serializer is valid")
            saved_user = serializer.save()
            # print("Saved user:", saved_user)

            # Return response with the saved user data
            return Response({'msg': "User Registered successfully", 'user': saved_user.email}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return a bad request response
        return JsonResponse({'msg': "Failed to create a user", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Log the error to help debugging
        print(f"Error: {e}")
        return JsonResponse({'msg': "Something went wrong while creating a new user", 'error': str(e)}, status=500)



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
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def update_or_delete_or_get_user_details(request,email):

# Trying to find the user from provided user_id
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message":"Failed to find the user"},status=400)
    
    if request.method == 'GET':
        foundUser = UserSerializer(user)
        return JsonResponse(foundUser.data,status=status.HTTP_200_OK)
    
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
        return JsonResponse({"message":"User deleted successfully"},status=status.HTTP_204_NO_CONTENT)

