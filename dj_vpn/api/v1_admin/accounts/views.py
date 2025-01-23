from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import mixins

from vpn.utils.paginations import AdminPagePagination
from . import serializers
from accounts.models import User, ContentDevice, OneDayLeftUser


class AdminAddUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.AdminUserAddSerializer
    permission_classes = [IsAdminUser]


class AdminUserProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.AdminUserProfileSerializer
    permission_classes = [IsAdminUser]
    pagination_class = AdminPagePagination


class AdminUserContentDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdminUserContentDeviceSerializer
    permission_classes = [IsAdminUser]
    pagination_class = AdminPagePagination

    def get_queryset(self):
        return ContentDevice.objects.select_related('user').filter(user=self.kwargs['user_pk'])

    def get_serializer_context(self):
        return {'user_pk': self.kwargs['user_pk']}


class OneDayLeftUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = OneDayLeftUser.objects.all()
    serializer_class = serializers.OneDayLeftUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = AdminPagePagination
