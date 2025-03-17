from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
import uuid
# Create your models here.
class User(models.Model):
    GENDER_CHOICES = {
        "M":"Male",
        "F":"Female",
        "O":"Others"
    }

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    phone_number = models.BigIntegerField(default=0000000000)
    password = models.CharField(max_length=255,default='')
    dob = models.DateField(default='1999-1-1')
    profile_photo = CloudinaryField(resource_type='image', folder='SkillSync/profile_photo', blank=True)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICES,default='')
    createdAt = models.DateTimeField(default=timezone.now)
    bio = models.TextField(default='',max_length=500)


class SkillPost(models.Model):

    post_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    post_name = models.CharField(max_length=500)
    post_description = models.TextField(max_length=10000)
    post_media = CloudinaryField(folder="SkillSync/post_media",blank=True)
    post_tags = models.CharField(max_length=100,blank=True)
    post_owner = models.ForeignKey(User,on_delete=models.CASCADE)
    post_likes = models.IntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)


class SkillCategory(models.Model):
    """
    Model for skill categories (e.g., Programming Languages, Web Development, etc.)
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For storing icon name/class
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Skill Categories"


class Skill(models.Model):
    """
    Model for individual skills
    """
    LEVEL_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} ({self.level})"
    
    class Meta:
        unique_together = ('name', 'user')  # A user can't have the same skill twice


class SkillEndorsement(models.Model):
    """
    Model for skill endorsements
    """
    id = models.AutoField(primary_key=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='endorsements')
    endorsed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='endorsements_given')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.skill.name}"
    
    class Meta:
        unique_together = ('skill', 'endorsed_by')  # A user can endorse a skill only once


