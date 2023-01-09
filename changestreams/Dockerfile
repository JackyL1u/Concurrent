FROM python:3.7

RUN mkdir /application
WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install redis

COPY . .