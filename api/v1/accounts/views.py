from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import views
from rest_framework.response import Response

from accounts.enums import AccountStatus
from accounts.models import User, ContentDevice, PrivateNotification
from vpn.utils.create_refresh_token import get_token_refresh_token
from vpn.utils.paginations import CommonPagination, AdminUserProfilePagination
from vpn.utils.permissions import NotAuthenticated
from . import serializers
from .serializers import ContentDeviceSerializer, PrivateNotificationsSerializer, VolumeUsageSerializer
from vpn.utils.status_code import ErrorResponse

class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [NotAuthenticated]


class UserProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdminUserProfileSerializer
    pagination_class = AdminUserProfilePagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        if 'pk' in self.kwargs and self.request.user.is_staff:
            return self.queryset.filter(id=self.kwargs['pk'])
        if 'pk' in self.kwargs:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset.filter(id=self.request.user.id)
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return serializers.ListUserProfileSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.UpdateUserProfileSerializer
        return super().get_serializer_class()


class LoginApiView(views.APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        device_number = request.data.get('device_number')
        user = authenticate(username=username, password=password, request=request)

        if user:
            refresh = get_token_refresh_token(user, device_number)
            response = Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            response.set_cookie(
                key='token', value=str(refresh), httponly=True, secure=True, samesite='Lax'
            )
            user.number_of_login += 1
            user.save()
            return response
        return Response({"detail": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


class ContentDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = ContentDeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContentDevice.objects.filter(user=self.request.user)

    # def get_permissions(self):
    #     if self.request.method not in permissions.SAFE_METHODS:
    #         return [IsAdminUser()]
    #     return super().get_permissions()


class PrivateNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = PrivateNotificationsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        return PrivateNotification.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()


# class LogoutApiView(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = serializers.LogoutSerializer

# def show_request(request):
#     return request


class VolumeUsageApiView(views.APIView):
    serializer_class = VolumeUsageSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.accounts_status == AccountStatus.ACTIVE:
            request.user.volume_usage += serializer.validated_data['volume_usage']
            request.user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(ErrorResponse.USER_USAGE_LIMIT, status=status.HTTP_400_BAD_REQUEST)
