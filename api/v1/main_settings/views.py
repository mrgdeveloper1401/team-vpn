from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from main_settings.models import PublicNotification, UtilsApps
from rest_framework import permissions

from vpn.utils.paginations import CommonPagination
from .serializers import PublicNotificationSerializer, AppSettingsSerializer


class PublicNotificationViewSet(viewsets.ModelViewSet):
    queryset = PublicNotification.objects.all()
    serializer_class = PublicNotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()


class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = UtilsApps.objects.all()
    serializer_class = AppSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()
