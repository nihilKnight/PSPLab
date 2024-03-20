# Sina news crawling bot (enable Cycle, Incremental and multi-page crawling)

## Brief

A crawling bot for [sina news](https://www.sina.com.cn), enabling **Cycle**, **Incremental**, **Multi-page** crawling. 

This bot is written for the BUAA-SCST PPS Lab.

## Build with docker

1. First, create a customized docker subnet 182.17.0.0/16 for communication between `redis` and `sina_bot`:
```
$ docker network create --subnet=182.17.0.0/16 sina_bot_net 
```

2. Run the `redis` container (from docker hub):

```
$ docker run --net sina_bot_net --ip 182.17.0.10 -d -p 6379:6379 -v %cd%/data:/data redis
```

3. Build the `sina_bot` image:

```
$ docker build . -t sina_bot:v2
```

4. Run the `sina_bot` container:

```
$ docker run --net sina_bot_net --ip 182.17.0.11 -d -p 9090:9090 -v %cd%:/sina_bot sina_bot:v2
```

## Build with local environment

1. First, modify `spiders/sina_spider:line 23` to:

```
23:    r = connect_to_redis()
```

2. Start redis (through docker or installation):

```
$ docker run -d -p 6379:6379 redis
```

3. Then execute the `run.py`:

```
$ python3 run.py
```
