FROM python:3.12-alpine

# test in local
#FROM dj:1.1.0

WORKDIR /home/app

COPY . /home/app

RUN apk --update --upgrade

RUN pip install --upgrade pip && \
    pip install -r ./requirements/production.txt

#test in local
# RUN pip install --upgrade pip

RUN adduser -D -H mg && \
    chown -R mg:mg /home/app && \
    chmod -R 755 /home/app

USER mg

ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "/home/app/start.sh"]