FROM python:3.7

RUN mkdir /application
WORKDIR /application

RUN pip install redis
RUN pip install "uvicorn[standard]"
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .
