from django.urls import path
from tweets import views

urlpatterns = [
    path('user/', views.list_users),
    path('user/<str:email>/',views.update_or_delete_or_get_user_details)
]