from rest_framework import serializers

from configs.models import Country, Config
from subscriptions.models import UserConfig


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name', "ir_country_name", "country_code"]


class SimpleconfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['config']


class ConfigSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Config
        exclude = ['is_deleted', "deleted_at", "created_at", "updated_at"]


class UserConfigurationSerializer(serializers.ModelSerializer):
    config = SimpleconfigSerializer()
    country_name = serializers.CharField(source="config.country.country_name")
    ir_country_name = serializers.CharField(source="config.country.ir_country_name")
    country_code = serializers.CharField(source="config.country.country_code")

    class Meta:
        model = UserConfig
        fields = ["id", 'config', "is_active", "country_name", "ir_country_name", "country_code"]
