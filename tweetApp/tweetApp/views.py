from django.shortcuts import render
from django.http import HttpResponse

# Custom views goes here

def first_view(request):
    return render(request,'index.html')