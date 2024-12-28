FROM python:3.12-slim

WORKDIR /home/app

COPY . .
#COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN apt update  -y && \
    apt upgrade -y && \
    apt install python3 -y && \
    apt install postgresql -y && \
    apt install nginx -y &&\
    apt install python3-pip -y

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
