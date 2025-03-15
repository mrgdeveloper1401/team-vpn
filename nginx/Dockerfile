FROM nginx:1.27.1-alpine

RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static && \
    mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se

COPY ./fullchain.pem /etc/letsencrypt/live/apppanel.paradox.com.se/
COPY ./privkey.pem.pem /etc/letsencrypt/live/apppanel.paradox.com.se/
