"""
URL configuration for vpn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
# from jet_django.urls import jet_urls
from debug_toolbar.toolbar import debug_toolbar_urls
from vpn.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views

api_url = [
    path('auth/', include("api.v1.accounts.urls", namespace='accounts')),
    path('config/', include("api.v1.configs.urls", namespace='configs')),
    path('main_settings/', include("api.v1.main_settings.urls", namespace='main_setting')),
]

admin_api = [
    path('admin_auth/', include("api.v1_admin.accounts.urls", namespace='admin_auth')),
    path('admin_config/', include("api.v1_admin.configs.urls", namespace='admin_config')),
]
swagger_urls = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]

urlpatterns = [
    # path('push_notification/', views.index, name='push_notification'),
    path('admin/', admin.site.urls),
    # path('jet_api/', include('jet_django.urls')),

] + api_url + swagger_urls + admin_api


if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
