from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', "password", "confirm_password"]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": _("invalid input")}, code=101)
        return data


class ListUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', "email", "mobile_phone", "first_name", "last_name", "birth_date", "account_type",
                  "accounts_status", "is_active", "date_joined"]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "email", "mobile_phone", "first_name", "last_name", "birth_date"]


class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', "user_permissions"]
