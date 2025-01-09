from django.urls import path
from tweets import views

urlpatterns = [
    path('user/', views.list_users),
    path('user/<str:email>/',views.update_or_delete_or_get_user_details),  # <type:name> is the way of defining request param in django
    path('login/',views.login_view),
    path('logout/',views.logout_view)
]