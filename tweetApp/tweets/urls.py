from django.urls import path
from tweets import views

urlpatterns = [
    path('',views.tweet_view,name='tweet'),
    path('profile/',views.profile_view,name='profile'),
    path('profile/view/',views.edit_profile_view,name='edit_profile'),
    # path('profile/edit/',views.edit_profile_view,name='edit_profile'),
]