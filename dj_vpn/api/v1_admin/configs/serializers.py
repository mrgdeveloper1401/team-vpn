from rest_framework import serializers

from dj_vpn.configs.models import Config, Country


class AdminCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AdminConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'
