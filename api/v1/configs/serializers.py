from rest_framework import serializers

from configs.models import Country, Config
from subscriptions.models import UserConfig


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['is_deleted', "deleted_at"]


class SimpleconfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['config']


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        exclude = ['is_deleted', "deleted_at"]


class UserConfigurationSerializer(serializers.ModelSerializer):
    config = SimpleconfigSerializer()

    class Meta:
        model = UserConfig
        exclude = ['created_at', "updated_at", "is_deleted", "deleted_at"]
