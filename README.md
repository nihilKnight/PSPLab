# Easy Flask Web app


## Intro

This project is written for BUAA CST PSP LAB7.

This web app features: 

- Easy Login/Registration;

- Different views on different users;

- Easy Relationship tables.

## QuickStart

1. Via `Docker`:

```shell
$ docker build . -t flask_app:v1
$ docker run -p 5000:your_local_port flask_app:v1
```

2. Via Virtual Environment:

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate         \\ In Ubuntu or other linux distri.
$ pip install -r requirements.txt
$ flask initdb --drop 
$ flask forge 
$ flask run 
```
