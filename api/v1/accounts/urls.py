from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import path


from . import views

app_name = 'accounts'
router = routers.DefaultRouter()
router.register(r'create_user', views.UserRegisterViewSet, basename="create_user")
router.register("user_profile", views.UserProfileViewSet, basename="user_profile")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns += router.urls
