FROM python:3.12-alpine

WORKDIR /home/app

COPY . /home/app

RUN apk add --update --upgrade --no-cache --virtual .tmp python3  \
    py3-pip  \
    redis  \
    celery  \
    postgresql  \
    nginx

RUN pip install --upgrade pip && \
    pip install -r ./requirements/production.txt

RUN adduser -D -H mg && \
    chown -R mg:mg /home/app && \
    chmod -R 755 /home/app && \
    pip install colorlog django-axes

USER mg

ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "/home/app/start.sh"]