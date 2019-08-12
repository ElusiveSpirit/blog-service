FROM python:3.7-alpine
LABEL maintainer="info@rubyfire.ru"

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps alpine-sdk gcc python3-dev musl-dev libffi-dev \
  && apk add postgresql-dev

# Requirements are installed here to ensure they will be cached.
RUN pip install -U pipenv setuptools
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --system --dev

WORKDIR /app
