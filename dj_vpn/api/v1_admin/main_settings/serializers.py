from rest_framework import serializers

from main_settings.models import UtilsApps


class UtilsAppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilsApps
        fields = '__all__'
