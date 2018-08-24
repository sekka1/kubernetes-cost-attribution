FROM gcr.io/google-appengine/python:2018-03-20-170502

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install virtualenv requests

ADD . /opt/app

WORKDIR /opt/app
