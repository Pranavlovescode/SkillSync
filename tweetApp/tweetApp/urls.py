"""
URL configuration for tweetApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_api, signup_api, logout_api
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('skill/', include('tweets.urls')),
    
    # Root URL - use the login API
    path('', login_api, name="home"),
    
    # REST API endpoints
    path('api/login/', login_api, name="api_login"),
    path('api/signup/', signup_api, name="api_signup"),
    path('api/logout/', logout_api, name="api_logout"),
    
    # Token authentication endpoint
    path('api/token-auth/', rest_views.obtain_auth_token, name='api_token_auth'),
]

# Add static URL configuration
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
