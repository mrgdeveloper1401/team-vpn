FROM nginx:1.27.1-alpine

RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static && \
    mkdir -p /etc/letsencrypt/live/apppanel.paradox.com.se

COPY . /etc/letsencrypt/live/apppanel.paradox.com.se/
