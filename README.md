# finaly

Python 3.x - Programming Language
Django 2.2.x - Powerful Web Framework
Django Rest Framework - Web API's
Jinja2 - Template Engine
Gunicorn - WSGI HTTP Server
PostgreSQL - PostgreSQL Database
NginX - High performance web server
Docker - Container Platform
ArvanCloud - Integrated Cloud Infrastructure
GitHub - Version Control
TravisCI - Continues Integration and Deployment
Postman - API Testing

Installation
First clone or download this project.

$ git clone https://github.com/cheestore-github/finaly.git
Then create docker network and volumes as below.

$ docker volume create cheestore_postgresql
$ docker volume create cheestore_static_volume
$ docker volume create cheestore_files_volume
$ docker network create nginx_network
$ docker network create cheestore_network
You need to create .env file in the project root file with default values.

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
Now run django and postgresql with docker-compose.

$ docker-compose up -d
Then run nginx container with docker-compose.

$ cd config/nginx/
$ docker-compose up -d
You can see cheestore web page on http://localhost, Template and API's are accessable by docker containers which you can see with below command.

$ docker ps -a
Output should be like this.

CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
fc6cc9d6d3d7        nginx_nginx         "nginx -g 'daemon of…"   2 hours ago         Up 2 hours          0.0.0.0:80->80/tcp       nginx
05103904dcb8        ae80efb17475        "gunicorn --chdir bl…"   2 hours ago         Up 2 hours          0.0.0.0:8000->8000/tcp   blogpy
4a183e90a9eb        postgres:10         "docker-entrypoint.s…"   2 hours ago         Up 2 hours          0.0.0.0:5432->5432/tcp   blogpy
