FROM python:3.12.1-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY . /app/

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development


CMD flask run --host=0.0.0.0 --debug

EXPOSE 5000
