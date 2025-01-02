from rest_framework import serializers

from configs.models import Country, Config


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['is_deleted', "deleted_at"]


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        exclude = ['is_deleted', "deleted_at"]
