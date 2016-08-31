FROM pypy:2-onbuild

# https://hub.docker.com/_/pypy/
# docker build -t web-redis .
# d run -it --rm --net=host web-redis

MAINTAINER Ivan Ribeiro Rocha <ivan.ribeiro@gmail.com>

COPY web-redis.py /usr/src/app/

EXPOSE 8080

CMD [ "pypy", "./web-redis.py" ]