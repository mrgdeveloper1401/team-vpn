from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

api_url = [
    path('auth/', include("dj_vpn.api.v1.accounts.urls", namespace='accounts')),
    path('config/', include("dj_vpn.api.v1.configs.urls", namespace='configs')),
    # path('main_settings/', include("dj_vpn.api.v1.main_settings.urls", namespace='main_setting')),
]

# admin_api = [
#     path('admin_auth/', include("dj_vpn.api.v1_admin.accounts.urls", namespace='admin_auth')),
#     path('admin_config/', include("dj_vpn.api.v1_admin.configs.urls", namespace='admin_config')),
#     path('admin_settings/', include('dj_vpn.api.v1_admin.main_settings.urls', namespace='admin_main_settings')),
# ]
swagger_urls = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]

urlpatterns = [
    path('admin/', admin.site.urls),

] + api_url + swagger_urls
