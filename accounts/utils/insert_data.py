import os

import psycopg2
from decouple import config
import pandas as pd
from django.contrib.auth.hashers import make_password
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vpn.envs.development")
# django.setup()
#
#
# def hash_password(password):
#     return make_password(password)
#
#
# DB_NAME = config("PUB_POSTDB_NAME", cast=str)
# DB_USER = config("PUB_POSTDB_USER", cast=str)
# DB_PASSWORD = config("PUB_POSTDB_PASSWORD", cast=str)
# DB_HOST = config("PUB_POSTDB_HOST", cast=str)
# DB_PORT = config("PUB_POSTDB_PORT", cast=int)
#
# conn = psycopg2.connect(
#     database=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )
# cursor = conn.cursor()
#
#
# data = pd.read_csv("user_data.csv")
#
# insert_query = """
# INSERT INTO auth_user (username, email, password, first_name, last_name, mobile_phone)
# VALUES (%s, %s, %s, %s, %s, %s)
# """
#
# for _, row in data.iterrows():
#     hashed_password = hash_password(row['password'])
#     values = (
#         row['username'],
#         row['email'],
#         hashed_password,
#         row['first_name'],
#         row['last_name'],
#         row['mobile_phone']
#     )
#     cursor.execute(insert_query, values)
#
# conn.commit()
#
# cursor.close()
# conn.close()
#
# print("تمام داده‌ها با موفقیت وارد شدند!")


read_data = pd.read_csv("MOCK_DATA(3).csv")
print(read_data['password'])
