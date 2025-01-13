from rest_framework_nested import routers
from rest_framework.urls import path
from django.urls import include
from . import views
from ..configs.views import AdminUserConfigViewSet

app_name = 'auth_admin'
router = routers.DefaultRouter()

router.register('user_profile', views.AdminUserProfileViewSet, basename='admin_user_profile')
router.register(r'add_user', views.AdminAddUserViewSet, basename='admin_user_add')

profile_router = routers.NestedDefaultRouter(router, 'user_profile', lookup='user')
profile_router.register('device', views.AdminUserContentDeviceViewSet, basename='admin_user_content_device')
profile_router.register('config', AdminUserConfigViewSet, basename="admin_user_config")

urlpatterns = [
    path('', include(profile_router.urls))
] + router.urls
