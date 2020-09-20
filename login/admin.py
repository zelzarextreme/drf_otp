from django.contrib import admin
from .models import UserLogin,UserOTP

# Register your models here.
admin.site.register(UserLogin)
admin.site.register(UserOTP)
