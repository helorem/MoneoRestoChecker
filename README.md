# moneoresto_checker

## Description
A new user interface for MoneResto data, based on the Android app API. A Python server fetch data, save it in a sqlite db and serve json.
The Ui is full HTML/CSS/JavaScript.

## Configuration
You have to edit the file src/api.moneoresto-checker.conf. By default, it use the fakeserver (tools/fakeserver.py) to simulate data.

## Requirement
This project was optimized for Nginx. It could run with another WebServer, but not the deploy system.

Morover, you should have a "default" site enabled.

The container system is based on Docker.
```bash
sudo apt-get install docker.io
```

You have to create a bin dir in the repo
```bash
cd MoneoResotChecker
mkdir bin
```

## Usage

### make deb
Create de .deb file of the project.

### make deploy
Create a Docker image of the project, ready to production. it will create and use the DEB file.

### make run
Run the Docker container, ready to production

### make install_nginx
Modify the default site of Nginx to add a redirection to the container

### make deploy-all
Deploy, run and install Nginx conf

### make deploy-dev
Create a Docker image of the project for dev purpose. The source folder is mounted into the container

### make run-dev
Run the Docker container for dev purpose

### make deploy-dev-all
Deploy and run in dev mode, then install Nginx conf

