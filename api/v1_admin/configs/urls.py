from rest_framework_nested import routers
from rest_framework.urls import path
from django.urls import include

from . import views


app_name = 'admin_config'
router = routers.DefaultRouter()
router.register('country', views.AdminCountryViewSet, basename='country')

country_router = routers.NestedDefaultRouter(router, 'country', lookup="country")
country_router.register('config', views.AdminConfigViewSet, basename='config')

urlpatterns = [
    path('', include(country_router.urls))
] + router.urls
