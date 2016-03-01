FROM centos

# MINIMAL VERSION
# docker build -t pyenv .

MAINTAINER Ivan Ribeiro Rocha <ivan.ribeiro@gmail.com>

ENV PYENV_VERSION 2.7

RUN mkdir -p /opt/python/cpython

COPY root /root/

RUN yum install -y vim ruby-devel libev-devel gcc gcc-c++ rpm-build make python-psutil python-gevent \
                   python-websocket-client python-requests python-setuptools \
                   python-devel python-virtualenv python-simplejson \
    && gem install fpm \
    && virtualenv /opt/python/cpython/dev \
    && source /opt/python/cpython/dev/bin/activate \
    && pip install ansible beautifulsoup4 boto3 geopy gevent iptools jsonschema nltk psutil \
                   pycrypto pyinstaller python-geohash redis requests simplejson textblob \
                   websocket-client
