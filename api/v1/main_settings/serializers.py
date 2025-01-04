from rest_framework import serializers

from main_settings.models import PublicNotification, UtilsApps


class PublicNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicNotification
        exclude = ['is_deleted', "deleted_at"]


class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilsApps
        exclude = ['is_deleted', "deleted_at"]
