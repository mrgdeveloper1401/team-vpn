from rest_framework import routers

from . import views

app_name = 'admin_main_settings'

router = routers.DefaultRouter()
router.register(r'main_settings', views.UtilsAppsViewSet, basename='main_settings')

urlpatterns = router.urls
