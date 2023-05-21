
FROM python:3.11

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg && pip install -r requirements.txt
COPY . /app/
