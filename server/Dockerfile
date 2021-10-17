FROM python:3.9.3-alpine
RUN apk update && \
  apk add --virtual build-base gcc g++ python3-dev libressl-dev musl-dev libffi-dev && \
  apk add postgresql-dev && \
  apk add netcat-openbsd py-pip jpeg-dev zlib-dev

WORKDIR /api
COPY requirements.txt /api

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
