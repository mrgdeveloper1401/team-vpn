from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from dj_vpn.configs.models import Country, Config
from dj_vpn.vpn.utils.paginations import AdminPagePagination
from . import serializers


class AdminCountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = serializers.AdminCountrySerializer
    pagination_class = AdminPagePagination
    permission_classes = [IsAdminUser]


class AdminConfigViewSet(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = serializers.AdminConfigSerializer
    pagination_class = AdminPagePagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Config.objects.select_related('country').filter(country_id=self.kwargs['country_pk'])

