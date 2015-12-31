# PredictionIO Morality Classification

Current version: v0.1.1

## Introduction

This is a repository to classify user's morality of their loan credit, it is based on PredictionIO's official classification template, and has integrated Apache Spark MLlib's Naive Bayes algorithm by default.

## Version

version is built in this format: vx.y[.z]

x: API version changed, tech stack changed.  
y: New feature/api introduced, code architechure changed.  
z: Bug fixed, small feature/improvment.

## Develop

We use [docker](www.docker.com) to manage our environment. And this project run on [PredictionIO](https://prediction.io/).

### Install docker

Use following shell command:
```shell
$ wget -qO- https://get.docker.com/ | sh
```

Our PredictionIO docker image is based on Spark 1.5.1, with python 3.4, and Prediction's version is 0.9.4. For more detail, see `dockerfile/dockerfile`.

## Entry script

We use docker for developing, testing and deploying, so we build start script, see `pio-mc.sh`.

```shell
$ sudo ./pio-mc.sh
Usage:
./pio-mc.sh <Command>

Command:
  - start
  - newapp
  - build
  - train
  - deploy
  - example <access_key>
  - mysql
  - status
  - stop
```

### Usage

**Note**: use `sodu` or run script under root permission.  
**Note**: create a directory named `jars` in the path of repository, and put mysql-connector jar for Spark into it. We use `mysql-connector-java-5.1.36-bin.jar`, you can use other version of connector, see [offical site](http://dev.mysql.com/downloads/file/?id=460363).
**Note**: we use mysql to store our data, so you need to create a mysql database, and edit prediction's config, see step.1. Or you can just use `mysql` command of our entry script to start a mysql docker container if you like.

1. into `./conf/prediction` to edit the config of PredictionIO itself in `pio-env.sh` and log config of Spark in `log4j.properties`.
2. Usually, use `start` command to start docker container and build up each work directorise.
3. Create a new application, using `newapp` command.  
    3.1. In test case, you can use `example` command, for more detail, see `pio-mc.sh`.  
    3.2. Use `status` command to see if everything goes well.
4. Use `build` command to build template. **Note**: the first time of running will take a long time.
5. Use `train` and `deploy` to start train and deploy.

**Note**: After a series of previous operation, if you restart the script after removed the docker container, you don't need to run `build` command at all. 

## Change log

### v0.1.1
* update README, add entry script usage.

### v0.1
* add base code. Using PredictionIO's official classification template.