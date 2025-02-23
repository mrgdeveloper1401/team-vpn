from rest_framework_nested import routers
from rest_framework.urls import path
from django.urls import include
from . import views

app_name = 'auth_admin'
router = routers.DefaultRouter()

router.register('user_profile', views.AdminUserProfileViewSet, basename='admin_user_profile')
router.register(r'add_user', views.AdminAddUserViewSet, basename='admin_user_add')
router.register("one_day_left_user", views.OneDayLeftUserViewSet, basename='one_day_left_user')

profile_router = routers.NestedDefaultRouter(router, 'user_profile', lookup='user')
profile_router.register('device', views.AdminUserContentDeviceViewSet, basename='admin_user_content_device')

urlpatterns = [
    path('', include(profile_router.urls))
] + router.urls
