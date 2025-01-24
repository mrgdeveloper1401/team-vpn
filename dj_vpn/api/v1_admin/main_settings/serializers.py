from rest_framework import serializers

from dj_vpn.main_settings.models import UtilsApps


class UtilsAppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilsApps
        fields = '__all__'
