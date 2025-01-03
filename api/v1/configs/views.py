from rest_framework import viewsets, permissions, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from configs.models import Country, Config
from vpn.utils.paginations import CommonPagination
from .serializers import CountrySerializer, ConfigSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.filter(is_active=True)
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()
    
    def get_queryset(self):
        if "country_pk" in self.kwargs:
            return Config.objects.filter(country_id=self.kwargs["country_pk"])
        return super().get_queryset()


class FreeConfigViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Config.objects.filter(is_free=True)
    serializer_class = ConfigSerializer
    # pagination_class = CommonPagination
