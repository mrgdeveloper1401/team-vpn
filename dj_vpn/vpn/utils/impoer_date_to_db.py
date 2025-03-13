import pandas as pd
import os
import django
# import psycopg2 as postgresql
# from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpn.envs.vpn.envs.development")

django.setup()


from configs.models import Country
# from configs.models import Config
# from main_settings.models import PublicNotification

country_data = pd.read_csv('data_db/country.csv')
# for i in country_data.values:
#     print(i)

data_country = [
    Country(
        en_country_name=i[0],
        country_code=i[1],
    )
    for i in country_data.values
]

# pub_notification_data = pd.read_csv("data_db/public_notification.csv")
# pub_notif_list = [
#     PublicNotification(
#         title=i[0],
#         body=i[1],
#         is_active=i[2]
#     )
#     for i in pub_notification_data.values
# ]

# read_config_data = pd.read_csv("data_db/config.csv")
# config_list = [
#     Config(
#         country_id=i[0], config=i[1], is_free=i[2], is_active=i[3], price=i[4]
#     )
#     for i in read_config_data.values
# ]

# connection_database = {
#     "dbname": config("PUB_POSTDB_NAME", cast=str),
#     "user": config("PUB_POSTDB_USER", cast=str),
#     "password": config("PUB_POSTDB_PASSWORD", cast=str),
#     "host": config("PUB_POSTDB_HOST", cast=str),
#     "port": config("PUB_POSTDB_PORT", cast=str),
# }

Country.objects.using("default").bulk_create(data_country)
# PublicNotification.objects.using("second_db").bulk_create(pub_notif_list)
# Config.objects.using("default").bulk_create(config_list)
