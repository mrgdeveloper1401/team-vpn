#!/bin/bash

sudo docker-compose down
git pull
docker-compose up --build -d