FROM gcr.io/google-appengine/python:2018-03-20-170502

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install virtualenv requests prometheus_client schedule

ADD . /opt/app

WORKDIR /opt/app

RUN mkdir /opt/cost-attribution-output
