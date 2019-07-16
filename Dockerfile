FROM ubuntu:16.04
MAINTAINER BingJing Chang <bxxxjxxg@gmail.com>

RUN apt-get update \
 && apt-get install -y python3 python3-pip git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install git+https://github.com/bxxxjxxg/pyicloud.git

ADD scripts/backup.py /main.py
RUN mkdir -p /Downloads && chmod +x /main.py

ENV TZ 'Asia/Taipei'
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENTRYPOINT ["/main.py"]
