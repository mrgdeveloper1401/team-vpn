from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.response import Response
from django.db.models import F

from dj_vpn.accounts.enums import AccountStatus
from dj_vpn.accounts.models import User, ContentDevice, PrivateNotification
from dj_vpn.vpn.utils.create_refresh_token import get_token_refresh_token
from dj_vpn.vpn.utils.paginations import CommonPagination
from dj_vpn.vpn.utils.permissions import NotAuthenticated
from . import serializers
from .serializers import ContentDeviceSerializer, PrivateNotificationsSerializer, VolumeUsageSerializer
from dj_vpn.vpn.utils.status_code import ErrorResponse


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [NotAuthenticated]


class UserProfileViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return serializers.GetUserProfileSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.UpdateUserProfileSerializer
        return super().get_serializer_class()


class UserProfileApiView(views.APIView):
    serializer_class = serializers.GetUserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = User.objects.get(username=request.user.username)
        serializer = self.serializer_class(query)
        if query.accounts_status == AccountStatus.LIMIT:
            response = Response(data={"message": "limit for today reached"}, status=status.HTTP_403_FORBIDDEN)
        elif query.accounts_status == AccountStatus.EXPIRED:
            response = Response(data={"message": "usage limit reached"}, status=status.HTTP_403_FORBIDDEN)
        else:
            response = Response(serializer.data, status=status.HTTP_200_OK)
        return response


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
            user.fcm_token = serializer.validated_data['fcm_token']
            user.save()
            return response
        return Response({"detail": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


class ContentDeviceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ContentDeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContentDevice.objects.filter(user=self.request.user)


class PrivateNotificationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PrivateNotificationsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        return PrivateNotification.objects.filter(user=self.request.user)


# class LogoutApiView(viewsets.GenericViewSet, mixins.CreateModelMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = serializers.LogoutSerializer

# def show_request(request):
#     return request


class VolumeUsageApiView(views.APIView):
    serializer_class = VolumeUsageSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(username=serializer.validated_data['username']).only("username")
        if user:
            if user.first().accounts_status == AccountStatus.ACTIVE:
                user.update(
                    volume_usage=F('volume_usage') + serializer.validated_data['volume_usage'],
                    all_volume_usage=F("all_volume_usage") + serializer.validated_data['volume_usage'],
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("DISCONNECT", status=status.HTTP_400_BAD_REQUEST, content_type="text/plain")
        return Response("USER NOT FOUND", status=status.HTTP_400_BAD_REQUEST)


class UpdateConnectionApiView(views.APIView):
    """
    this api update field is_connected_user
    you have error 400, when two something was happened
    if a user account is not active
    if field is_connected_user is active
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.accounts_status == AccountStatus.ACTIVE and not user.is_connected_user:
            user.is_connected_user = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(ErrorResponse.USER_USAGE_LIMIT, status=status.HTTP_400_BAD_REQUEST)


class DeactivateUserConnectionApiView(views.APIView):
    """
    this api deactivate field is_connected_user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_connected_user:
            user.is_connected_user = False
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(ErrorResponse.FIELD_NOT_ACTIVE)
