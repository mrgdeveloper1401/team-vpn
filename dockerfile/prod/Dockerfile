FROM python:3.12-alpine

WORKDIR /home/app

COPY . .
#COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add postgresql && \
    apk add py3-pip && \
    apk add nginx

RUN pip install --upgrade pip && \
    pip install -r ./requirements/production.txt
RUN adduser -D -H vpn && \
    chown -R vpn:vpn /home/app
USER vpn

ENV PYTHONDONOTWRITEODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]