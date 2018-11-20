FROM gcr.io/google-appengine/python:2018-11-05-103343

RUN apt-get update && apt-get install -y python3-pip g++ python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv requests prometheus_client schedule rook

ADD . /opt/app

WORKDIR /opt/app

RUN mkdir /opt/cost-attribution-output
