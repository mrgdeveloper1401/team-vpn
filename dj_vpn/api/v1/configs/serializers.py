from rest_framework import serializers

from dj_vpn.configs.models import Country, Config
from dj_vpn.subscriptions.models import UserConfig


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'en_country_name', "fa_country_name", "country_code"]


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
    config = serializers.CharField()
    en_country_name = serializers.CharField(source="config.country.en_country_name")
    fa_country_name = serializers.CharField(source="config.country.fa_country_name")
    country_code = serializers.CharField(source="config.country.country_code")

    class Meta:
        model = UserConfig
        fields = ["id", 'config', "en_country_name", "fa_country_name", "country_code"]
