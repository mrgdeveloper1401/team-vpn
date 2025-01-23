# from google.oauth2 import service_account
# import google.auth.transport.requests
# import os
# from pathlib import Path
#
# base_dir = Path(__file__).resolve().parent
#
# credentials = service_account.Credentials.from_service_account_file(
#     os.path.join(base_dir, "team-vpn-702b2-firebase-adminsdk-ykycw-7d32345a5c.json"),
#     scopes=['https://www.googleapis.com/auth/firebase.messaging']
# )
#
# request = google.auth.transport.requests.Request()
# credentials.refresh(request)
#
# # توکن دسترسی
# access_token = credentials.token
# print("Access Token:", access_token)
