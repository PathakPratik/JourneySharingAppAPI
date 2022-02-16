FROM python:3.9.7

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* /app

RUN cd /app && pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . . 

ADD flask_confirmed_users.sql /var/lib/mysql

#ADD flask_confirmed_users.sql /docker-entrypoint-initdb.d

CMD python app.py