FROM mysql:latest

ENV MYSQL_DATABASE=flask
ENV MYSQL_ROOT_PASSWORD=secret_password

ADD flask_confirmed_users.sql /docker-entrypoint-initdb.d

EXPOSE 3306