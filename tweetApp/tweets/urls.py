from django.urls import path
from tweets import views

urlpatterns = [
    path('',views.tweet_view,name='tweet'),
    path('profile/',views.profile_view,name='profile'),
]