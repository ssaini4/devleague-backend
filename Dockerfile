FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    && python -m pip install --upgrade pip setuptools \
    && mkdir -p /workspace/devleague

WORKDIR /workspace/devleague
COPY ./requirements.txt /workspace/devleague/requirements.txt

RUN pip install -r ./requirements.txt \
    && apt-get clean

COPY . /workspace/devleague/