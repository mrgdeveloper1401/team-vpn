FROM python:3.12-slim

WORKDIR /home/app

COPY . .

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install python3 -y&& \
    apt-get install postgresql -y&& \
    apt-get install nginx -y&& \
    apt-get install python3-pip -y

RUN adduser --disabled-password --gecos "" mg && \
    chown -R mg:mg /home/app && \
    chmod -R 755 /home/app

USER mg

RUN pip install --upgrade pip && \
    pip install -r ./requirements/production.txt
ENV PYTHONDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN chmod +x /home/app/start.sh

ENTRYPOINT ["/home/app/start.sh"]
