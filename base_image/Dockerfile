FROM python:3.12-alpine

COPY requirements.txt .

ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk upgrade && \
    apk add bash && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

