FROM python:3.12-slim

WORKDIR /home/app
COPY . .

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y python3 && \
    apt install postgresql -y && \
    apt install nginx -y && \
    apt install python3-pip -y && \
    apt install vim -y

RUN pip install --upgrade pip && \
    pip install -r ./requirements/production.txt


ENV PYTHONDONOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]
