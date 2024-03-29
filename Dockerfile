FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app
COPY requirements.txt /app
RUN --mount=type=cache,target=/home/progmatic99/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app
