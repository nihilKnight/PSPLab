# Sina News Crawling Bot 

## Brief

A crawling bot for [sina news](https://www.sina.com.cn), enabling **Cycle**, **Incremental**, **Multi-page** crawling. 

This bot is written for the BUAA-SCST PSP Lab.

## QuickStart

- with `venv`

```
$ python3 -m venv .venv
$ .venv/Scripts/activate.bat                                              # for windows
$ pip3 install -r requirements.txt
$ python3 run.py [sina_spider / sina_incremental_spider]                  # normal / incremental
$ docker run -d -p 6379:6379 redis                                        # pull and run redis, and map its port to localhost:6379
$ python3 schedule_run.py [sina_spider / sina_incremental_spider]         # normal timing / incremental timing
```

- with `docker`

```
$ docker build . -t sina_bot:v2
$ docker network create --subnet=182.17.0.0/16 sina_bot_net               # create a sub net for the bot and redis
$ docker run --net sina_bot_net --ip 182.17.0.10 -d -p 6379:6379 redis
$ docker run --net sina_bot_net --ip 182.17.0.11 -d -p 6080:6080 -v %cd%:/sina_bot sina_bot:v2
                                                                          # for windows, mount sina_bot:v2 to current dir
$ docker ps                                                               # show the containers on running
```

