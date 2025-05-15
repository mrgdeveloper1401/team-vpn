# FROM nginx:1.27.1-alpine
FROM docker.arvancloud.ir/nginx

RUN mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se

COPY . /etc/letsencrypt/live/apppanel.paradox.com.se/

RUN mkdir /vol