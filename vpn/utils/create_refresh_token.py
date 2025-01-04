from rest_framework_simplejwt.tokens import RefreshToken


def get_token_refresh_token(use, device_info):
    refresh = RefreshToken.for_user(use)
    refresh['device_number'] = device_info
    return refresh
