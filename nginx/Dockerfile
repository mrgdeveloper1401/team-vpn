FROM nginx:1.27.1-alpine

RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static

VOLUME /vol/static

COPY ./fullchain.pem /etc/letsencrypt/live/apppanel.paradox.com.se/fullchain.pem
COPY ./privkey.pem /etc/letsencrypt/live/apppanel.paradox.com.se/privkey.pem