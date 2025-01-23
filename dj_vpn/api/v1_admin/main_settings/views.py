from rest_framework import viewsets
from rest_framework import permissions

from . import serializers
from main_settings.models import UtilsApps


class UtilsAppsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UtilsAppsSerializer

    def get_queryset(self):
        if self.request.user.is_satff or self.request.user.is_supperuser:
            query = UtilsApps.objects.all()
        else:
            query = UtilsApps.objects.filter(is_main_settings=True)
        return query

    def get_permissions(self):
        if not permissions.SAFE_METHODS:
            perm = [permissions.IsAdminUser()]
        else:
            perm = [permissions.IsAuthenticated()]
        return perm
