from rest_framework import serializers
from .models import UserLogin


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserLogin
        fields=['phone','user']


    def create(self,validated_data):
         user=UserLogin.objects.create(**validated_data)
         return user   
