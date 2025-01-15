from django.http import HttpResponse
from django.shortcuts import render


def tweet_view(request):
    return render(request, 'tweet.html')


def profile_view(request):
    return render(request, 'profile.html')