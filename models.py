from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    phone=models.CharField(max_length=13,blank=False)
   
   
class UserOTP(models.Model):   
    phone=models.CharField(max_length=13,blank=False)
    otp=models.CharField(max_length=4,blank=False)
    is_verified=models.BooleanField(default=False)


