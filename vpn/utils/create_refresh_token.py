from rest_framework_simplejwt.tokens import RefreshToken


def get_token_refresh_token(user, device_info):
    refresh = RefreshToken.for_user(user)
    refresh['device_number'] = device_info
    return refresh
