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
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    password = models.CharField(max_length=255)
    dob = models.DateField(default='')
    profile_photo = CloudinaryField('peeptalks/profile_photo',blank=True)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICES,default='')
    createdAt = models.DateTimeField(default=timezone.now)


