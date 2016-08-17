# docker build -t webrest .
# docker run --name webrest --rm -p 8000:8000

FROM ubuntu

MAINTAINER Ivan Ribeiro Rocha <ivan.ribeiro@gmail.com>

RUN apt-get update && apt-get install -y libssl1.0 libexpat1 libffi6

RUN mkdir -p /opt/python/devpy

COPY devpy /opt/python/devpy
COPY pypy /opt/python/pypy

COPY webrest.py /opt/python/
COPY webrest.sh /opt/python/

WORKDIR /opt/python/

EXPOSE 8000

CMD ["./webrest.sh"]
