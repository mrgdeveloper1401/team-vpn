from rest_framework import routers

from . import views

app_name = 'main_setting'
router = routers.DefaultRouter()
router.register(r'public_notification', views.PublicNotificationViewSet, basename='public_notification')
# router.register('app_settings', views.AppSettingsViewSet, basename='app_settings')

urlpatterns = router.urls
