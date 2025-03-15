FROM nginx:1.27.1-alpine

RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static && \
    mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se/

VOLUME /vol/static

COPY ./nginx/fullchain.pem /etc/letsencrypt/live/apppanel.paradox.com.se/fullchain.pem
COPY ./nginx/privkey.pem /etc/letsencrypt/live/apppanel.paradox.com.se/privkey.pem
