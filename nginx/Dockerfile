FROM nginx:1.27.1-alpine

RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static

VOLUME /vol/static

COPY ./nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key