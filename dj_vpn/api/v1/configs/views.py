from rest_framework import viewsets, permissions, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from dj_vpn.configs.models import Country, Config
from .serializers import CountrySerializer, ConfigSerializer, ConfigurationSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
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
    queryset = Config.objects.select_related("country")
    serializer_class = ConfigSerializer
    # permission_classes = [IsAuthenticated]
    # pagination_class = CommonPagination


class ConfigListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ConfigurationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request_user_type = self.request.user.user_type
        if request_user_type == "a_user":
            return Config.objects.filter(is_active=True, config_type="tunnel_server").select_related("country")
        else:
            return Config.objects.filter(is_active=True, config_type="direct_server").select_related("country")
