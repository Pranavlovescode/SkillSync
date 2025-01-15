from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm,SignUpForm
from tweets.models import User
from django.contrib.auth import authenticate,login,logout

# Custom views goes here

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect('/tweet/')
            else:
                return HttpResponseRedirect('/')
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

def tweet_view(request):
    return render(request,'tweet.html')