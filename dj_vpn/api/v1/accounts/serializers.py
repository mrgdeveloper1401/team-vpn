from django.contrib.auth.password_validation import validate_password
from django.db.models import Count
from rest_framework.validators import ValidationError
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from dj_vpn.accounts.models import User, ContentDevice, PrivateNotification
from dj_vpn.vpn.utils.status_code import ErrorResponse


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


class GetUserProfileSerializer(serializers.ModelSerializer):
    day_left = serializers.SerializerMethodField()
    end_date_subscription = serializers.SerializerMethodField()
    remaining_volume_amount = serializers.SerializerMethodField()

    def get_day_left(self, obj):
        return obj.day_left

    def get_end_date_subscription(self, obj):
        return obj.end_date_subscription

    def get_remaining_volume_amount(self, obj):
        return obj.remaining_volume_amount

    class Meta:
        model = User
        exclude = ['password', "groups", "user_permissions", "is_superuser", "is_staff", "is_active", "deleted_at",
                   "is_deleted", "last_login"]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "mobile_phone", "first_name", "last_name", "birth_date"]


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
            username = attrs.get("username")
            device = ContentDevice.objects.get(user__username=username, device_number=device_number)
        except ContentDevice.DoesNotExist:
            user = User.objects.filter(username=username).first()
            if user:
                data = attrs.copy()
                del data['username']
                del data['password']
                del data['fcm_token']
                if user.number_of_max_device > user.user_device.count():
                    ContentDevice.objects.create(**data, user=user)
                else:
                    raise ValidationError(ErrorResponse.MAXIMUM_REACH)
            else:
                raise ValidationError(ErrorResponse.OBJECT_NOT_FOUND)
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


class VolumeUsageSerializer(serializers.Serializer):
    volume_usage = serializers.FloatField(
        help_text=_("حجم مصرفی به صورت مگابایت ارسال شود")
    )
