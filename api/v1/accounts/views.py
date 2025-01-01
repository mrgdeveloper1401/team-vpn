from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from vpn.utils.permissions import NotAuthenticated
from . import serializers


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [NotAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdminUserProfileSerializer

    def get_queryset(self):
        if "pk" in self.kwargs:
            return User.objects.filter(pk=self.request.user.pk)
        if self.request.user.is_staff:
            return User.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return serializers.ListUserProfileSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.UpdateUserProfileSerializer
        return super().get_serializer_class()
