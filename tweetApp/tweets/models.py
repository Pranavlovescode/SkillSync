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
    createdAt = models.DateTimeField(default=timezone.now)


