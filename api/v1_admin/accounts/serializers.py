from rest_framework.validators import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from accounts.models import User, ContentDevice
from vpn.utils.status_code import ErrorResponse


class AdminUserAddSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            "username", "password", "account_type", "accounts_status", "volume_choice", "volume", "number_of_days",
            "number_of_max_device", "confirm_password"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError(ErrorResponse.INVALID_INPUT)
        try:
            validate_password(attrs['password'])
        except Exception:
            raise ErrorResponse.INVALID_PASSWORD
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)


class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', "user_permissions"]
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "username": {"required": False},
            "password": {"required": False},
            "last_login": {"read_only": True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            try:
                check_password(attrs['password'])
            except Exception as e:
                raise ValidationError(e)
        return attrs


class AdminUserContentDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentDevice
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        user_id = self.context['user_pk']
        return ContentDevice.objects.create(user_id=user_id, **validated_data)
