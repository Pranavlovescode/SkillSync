from django.shortcuts import render
from django.http import HttpResponse

# Custom views goes here

def login_view(request):
    return render(request,'login.html') 

def signup_view(request):
    return render(request,'signup.html')