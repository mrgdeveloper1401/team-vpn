from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import ContentDevice


class CheckDeviceBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            get_token = request.headers.get("Authorization")
            split_token = get_token.split("Bearer")
            get_split_token = split_token[1]
            mine_token = AccessToken(get_split_token)
            device_number = mine_token.get('device_number')

            device = ContentDevice.objects.filter(device_number=device_number).last()
            if device and device.is_blocked:
                raise PermissionDenied("your device is blocked")
        response = self.get_response(request)
        return response
