FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt