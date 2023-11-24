from django.contrib.auth import get_user_model
from rest_framework import serializers


USER_MODEL = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL


class LoginUserSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UpdateUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
