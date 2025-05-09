from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import path
from rest_framework_simplejwt.views import TokenBlacklistView


from . import views

app_name = 'accounts'
router = routers.DefaultRouter()
# router.register(r'create_user', views.UserRegisterViewSet, basename="create_user")
router.register("user_profile", views.UserProfileViewSet, basename="user_profile")
router.register('content_device', views.ContentDeviceViewSet, basename="content_device")
router.register('private_notification', views.PrivateNotificationViewSet, basename="private_notification")

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user_profile/', views.UserProfileApiView.as_view(), name='user_profile_api_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', views.LoginApiView.as_view(), name='login'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('volume_usage/', views.VolumeUsageApiView.as_view(), name='volume_usage'),
    path('active_connection_user', views.UpdateConnectionApiView.as_view(), name='update_connection_user'),
    path('deactivate_connection_user/', views.DeactivateUserConnectionApiView.as_view(),
         name='deactivate_connection_user'),

    # path('show_request/', views.show_request, name='show_request'),
]

urlpatterns += router.urls
