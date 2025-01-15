from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import LoginForm,SignUpForm
from tweets.models import User
from .backends import EmailBackend
import logging
logger = logging.getLogger(__name__)

# Custom views goes here

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        print(username_or_email,password)
        logger.debug(f'User: {request.user}')  # Log the user object
        
        form = LoginForm(request.POST)

        custom_backend = EmailBackend()

        if form.is_valid():
            user = custom_backend.authenticate(request=request,username_or_email=username_or_email,password=password)
            print(f"User: {user}")
            if user:      
                request.session['user']=user.email
                return HttpResponseRedirect('/tweet/')
            else:
                form.add_error(None,'Invalid credentials')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

# Storing the data in the database
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(first_name,last_name,email,username,password)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.save()
            return HttpResponseRedirect('/tweet')
    else:
        form = SignUpForm()

    return render(request,'signup.html',{'form':form})

# def tweet_view(request):
#     return render(request,'tweet.html')