FROM ubuntu:latest

ADD . /app/flask_app

WORKDIR /app/flask_app

RUN apt-get update && apt-get -y install python3

RUN python3 -m venv .venv

RUN source .venv/bin/activate

RUN pip install -r requirements.txt

RUN flask initdb

RUN flask run

