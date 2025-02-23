from rest_framework import serializers

from dj_vpn.configs.models import Country, Config


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


class NestedCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['en_country_name', "fa_country_name", "country_code"]


class ConfigurationSerializer(serializers.ModelSerializer):
    en_country_name = serializers.CharField(source="country.en_country_name")
    fa_country_name = serializers.CharField(source="country.fa_country_name")
    country_code = serializers.CharField(source="country.country_code")

    class Meta:
        model = Config
        fields = ['id', "en_country_name", "fa_country_name", "country_code", "config", "config_type"]
