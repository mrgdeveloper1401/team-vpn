FROM python:3.12-alpine

WORKDIR /home/app

COPY . /home/app

RUN apk update && \
    apk upgrade && \
    apk add postgresql && \
    apk add python3 && \
    apk add py3-pip \
    apk add nginx

RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
