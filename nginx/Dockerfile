FROM nginx:1.27.1-alpine
#FROM docker.arvancloud.ir/nginx:1.27-alpine

RUN mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se

COPY nginx.conf /etc/nginx/

COPY . /etc/letsencrypt/live/apppanel.paradox.com.se/
