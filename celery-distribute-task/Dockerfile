FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

RUN mkdir /django_celery_test

WORKDIR /django_celery_test

# copy porject
COPY . .

RUN pip install -r requirements.txt