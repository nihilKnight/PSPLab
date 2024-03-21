FROM ubuntu:latest

WORKDIR /sina_bot

ADD . /sina_bot

EXPOSE 6080

RUN apt-get update && apt-get -y install python3 python3-pip

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "schedule_run.py"]
