#!/bin/bash

docker volume create --name=app_container

docker-compose up -d --build
