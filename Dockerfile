FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
RUN adduser -ms /bin/bash -u 1001 app
USER app

# Copy source files into application directory
COPY --chown=app:app . /app
WORKDIR /app
COPY requirements.txt /app
RUN --mount=type=cache,target=/home/progmatic99/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]