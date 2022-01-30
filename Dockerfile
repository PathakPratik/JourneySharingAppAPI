FROM python:3.9.7

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

ADD controllers /app/controllers
COPY constants.py /app
COPY app.py /app
RUN ls -lrt
CMD python app.py