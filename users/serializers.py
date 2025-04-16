from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists')

class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField()

class UserBaseSerializer(serializers.ModelSerializer):
    pass