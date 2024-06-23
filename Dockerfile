FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get -y install python3 python3-pip

EXPOSE 5000

CMD ["pip3", "install", "-r", "requirements.txt"]

CMD ["python3", "-m", "flask", "initdb"]

CMD ["python3", "-m", "flask", "forge"]

ENTRYPOINT ["python3", "-m", "flask", "run"]
