FROM python:3.7-alpine
LABEL maintainer="info@rubyfire.ru"

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps alpine-sdk gcc python3-dev musl-dev libffi-dev \
  && apk add postgresql-dev


RUN addgroup -S aiohttp \
    && adduser -S -G aiohttp aiohttp

# Requirements are installed here to ensure they will be cached.
RUN pip install -U pipenv setuptools
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock
RUN pipenv install --system --deploy

COPY ./config/prod/app/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown aiohttp /entrypoint

COPY ./config/prod/app/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown aiohttp /start


COPY . /app

USER aiohttp

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
