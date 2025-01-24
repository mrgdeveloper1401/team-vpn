from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from dj_vpn.accounts.models import ContentDevice


class CheckDeviceBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get_user = request.META.get("USER")
        if get_user:
            get_token = request.headers.get("Authorization")
            if get_token:
                split_token = get_token.split("Bearer ")
                get_split_token = split_token[-1]
                mine_token = AccessToken(get_split_token)
                device_number = mine_token.get('device_number')

                device = ContentDevice.objects.filter(device_number=device_number).last()
                if device and device.is_blocked:
                    return JsonResponse({'detail': "your device is blocked"}, status=status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)
        return response


class CheckLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
