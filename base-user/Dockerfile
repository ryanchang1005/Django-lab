FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /django_base_user

WORKDIR /django_base_user

# copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# copy porject
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "docker-entrypoint.sh" ]