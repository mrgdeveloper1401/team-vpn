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
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', views.LoginApiView.as_view(), name='login'),
    path('lockout/', views.show_block, name='show_blocked')
]

urlpatterns += router.urls
