from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import User, ContentDevice, PrivateNotification


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', "password", "confirm_password"]
        extra_kwargs = {
            "password": {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": _("invalid input")}, code=101)
        try:
            validate_password(data['password'])
        except Exception as e:
            raise e
        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)


class ListUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', "email", "mobile_phone", "first_name", "last_name", "birth_date", "account_type",
                  "accounts_status", "is_active", "date_joined", "volume", "volume_usage", "number_of_days"]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "email", "mobile_phone", "first_name", "last_name", "birth_date"]


class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', "user_permissions"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, style={'input_type': 'password'})


class ContentDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentDevice
        exclude = ['is_deleted', "deleted_at", "created_at", "updated_at"]
        extra_kwargs = {
            "user": {'read_only': True}
        }


class PrivateNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateNotification
        exclude = ['is_deleted', "deleted_at"]


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
