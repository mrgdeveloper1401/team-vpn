FROM nginx:1.27.1-alpine
#FROM docker.arvancloud.ir/nginx:1.27-alpine

RUN mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se

COPY fullchain.pem /etc/letsencrypt/live/apppanel.paradox.com.se/
COPY privkey.pem /etc/letsencrypt/live/apppanel.paradox.com.se/
