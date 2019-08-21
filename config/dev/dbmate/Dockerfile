FROM alpine

RUN apk update && apk add postgresql-client curl

RUN curl -fsSL -o /dbmate https://github.com/amacneil/dbmate/releases/download/v1.6.0/dbmate-linux-musl-amd64 && \
  chmod +x /dbmate

ENTRYPOINT ["/dbmate"]
