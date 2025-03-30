from django.urls import path, include
from tweets import views
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet, SkillPostViewSet

# Create a router for our API viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', SkillPostViewSet)

urlpatterns = [
    # Traditional views
    path('', views.tweet_view, name='skill'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/view/', views.edit_profile_view, name='edit_profile'),
    path('post/', views.create_new_post, name='skill_post'),
    path("skills-post/", views.create_new_skills, name="create_new_skills"),
    path("skills-category/", views.add_category, name="create_new_category"),
    path("get-skills-by-category/<str:category_id>/", views.get_skill_by_category, name="get_skills_by_category"),
    # API endpoints
    path('api/', include(router.urls)),
]