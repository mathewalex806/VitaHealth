from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


class User(AbstractUser):
    calorie_count = models.IntegerField(blank=True, null=True)
    allergies = models.TextField(max_length=20, blank=True, null= True)
    recipe = models.TextField(max_length=50, blank= True, null = True)

    
    def __str__(self):
        return f"{self.username}"
    
class Image(models.Model):
    user_img = models.ImageField(null=True, blank=True, upload_to="images/")