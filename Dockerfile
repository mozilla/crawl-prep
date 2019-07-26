FROM python:3.7

WORKDIR /opt/crawl-prep

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .
