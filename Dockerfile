FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

SHELL ["/bin/bash", "-c"]

EXPOSE 8000

WORKDIR /app


COPY . .

RUN  apt-get update -y && apt-get upgrade -y &&  pip install --upgrade pip \
    &&  pip install  --upgrade setuptools \
    &&  pip install  --no-cache-dir -r   requirements.txt


CMD python bot/echo1.py
