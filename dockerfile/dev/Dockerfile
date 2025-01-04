FROM python:3.12-alpine

WORKDIR /home/app

COPY ../../ /home/app

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add py3-pip

RUN pip install -r /home/app/requirements/base.txt

ENV PYTHONDONOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]
