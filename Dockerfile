FROM python:3-stretch

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install virtualenv requests

ADD . /opt/app

WORKDIR /opt/app
