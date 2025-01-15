from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import User, ContentDevice, PrivateNotification
from vpn.utils.status_code import ErrorResponse


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
            raise serializers.ValidationError(ErrorResponse.INVALID_INPUT, code=101)
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
        exclude = ['password', "groups", "user_permissions", "is_superuser", "is_staff", "is_active", "deleted_at",
                   "is_deleted", "last_login"]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "mobile_phone", "first_name", "last_name", "birth_date"]


class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', "user_permissions"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, style={'input_type': 'password'})
    device_number = serializers.CharField()
    ip_address = serializers.IPAddressField()
    device_model = serializers.CharField()
    device_os = serializers.CharField()
    fcm_token = serializers.CharField()

    def validate(self, attrs):
        try:
            device_number = attrs.get('device_number')
            device = ContentDevice.objects.get(user__username=attrs["username"], device_number=device_number)
        except ContentDevice.DoesNotExist:
            user = User.objects.get(username=attrs['username'])
            del self.initial_data['username']
            del self.initial_data['password']
            del self.initial_data['fcm_token']
            ContentDevice.objects.create(**self.initial_data, user=user)
        else:
            if device.is_blocked:
                raise ValidationError(ErrorResponse.LOGIN_BLOCKED)
            for key, value in self.initial_data.items():
                if hasattr(device, key):
                    setattr(device, key, value)
            device.save()
        return attrs


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
        exclude = ['is_deleted', "deleted_at", "user"]


# class LogoutSerializer(serializers.Serializer):
#     refresh_token = serializers.CharField()
#
#     def save(self, **kwargs):
#         pass


class VolumeUsageSerializer(serializers.Serializer):
    volume_usage = serializers.FloatField(
        help_text=_("حجم مصرفی به صورت مگابایت ارسال شود")
    )
