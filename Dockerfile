FROM python:3.9.7

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* /app

RUN cd /app && pipenv lock --keep-outdated --requirements > requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . . 

CMD python app.py