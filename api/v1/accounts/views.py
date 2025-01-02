from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import views
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from vpn.utils.paginations import AdminUserProfilePagination
from vpn.utils.permissions import NotAuthenticated
from . import serializers


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [NotAuthenticated]


class UserProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdminUserProfileSerializer

    # pagination_class = AdminUserProfilePagination

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     return self.queryset
        # if 'pk' in self.kwargs and self.request.user.is_staff:
        #     return self.queryset.filter(id=self.kwargs['pk'])
        if 'pk' in self.kwargs:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return serializers.ListUserProfileSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.UpdateUserProfileSerializer
        # return super().get_serializer_class()


class LoginApiView(views.APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password, request=request)

        # if user and is_already_locked(request):
            # raise PermissionDenied("your account blocked, please try agin after ten minute")

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"refresh": str(refresh), "access": str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            response.set_cookie(
                key='token', value=str(refresh), httponly=True, secure=True, samesite='Lax'
            )
            return response
        return Response({"detail": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


# show message django axes, When the user repeats too much
def show_block(request, credentials, *args, **kwargs):
    return JsonResponse({"message": "you blocked, please try agin after ten minute"},
                        status=status.HTTP_403_FORBIDDEN)
