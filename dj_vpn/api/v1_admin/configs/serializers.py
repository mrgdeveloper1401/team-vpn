from rest_framework import serializers

from dj_vpn.configs.models import Config, Country
from dj_vpn.subscriptions.models import UserConfig


class AdminCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AdminConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'


class AdminUserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = '__all__'
