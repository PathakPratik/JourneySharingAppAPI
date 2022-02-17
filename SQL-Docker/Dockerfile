FROM mysql:latest

ENV MYSQL_DATABASE=$MYSQL_DATABASE
ENV MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD

ADD flask_confirmed_users.sql /docker-entrypoint-initdb.d

EXPOSE 3306