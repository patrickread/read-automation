# syntax=docker/dockerfile:experimental

FROM python:3.10.1

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r ./requirements.txt
COPY requirements-dev.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r ./requirements-dev.txt

COPY . /app

ENV FLASK_APP app.py
ENV FLASK_ENV development

CMD ["flask", "run", "--host=0.0.0.0"]
