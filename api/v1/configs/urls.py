from django.urls import include
from rest_framework_nested import routers
from rest_framework.urls import path

from . import views

app_name = 'configs'
router = routers.DefaultRouter()
router.register(r'country', views.CountryViewSet, basename="country")
router.register('free_config', views.FreeConfigViewSet, basename="free_config")

country = routers.NestedDefaultRouter(router, r'country', lookup='country')
country.register(r'config', views.ConfigViewSet, basename="config")
country.register('free_config', views.FreeConfigViewSet, basename="free_config")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(country.urls)),
]
urlpatterns += router.urls
