FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add postgresql && \
    apk add py3-pip && \
    apk add nginx

RUN pip install --upgrade pip && \
    pip install -r ./requiremenets/development.txt

EXPOSE 8000

ENTRYPOINT = ["./start.sh"]