FROM python:3.8-slim-buster

LABEL Name=rest_service_rjewing Version=0.0.1
EXPOSE 5000

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install libjpeg-dev zlib1g-dev libfreetype6-dev ffmpeg dnsutils

COPY requirements.txt /usr/src/app
RUN  pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
