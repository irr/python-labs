#!/bin/bash

VERSION=0.1
NAME=pyenv

if [[ ! -z "$1" ]]; then
  NAME=$1
fi

if [[ ! -z "$2" ]]; then
  VERSION=$2
fi

RPM=${NAME}-${VERSION}-1.x86_64.rpm
PACKAGE=${RPM}

echo "building ${PACKAGE}"

rm -rf ${PACKAGE}

fpm -s dir -t rpm -n ${NAME} -v ${VERSION} --rpm-user root --rpm-group root \
    --prefix /opt/python/cpython \
    -m "ivan.ribeiro@gmail.com" \
    -C /opt/python/cpython && \
rpm -q -filesbypkg -p ${PACKAGE}
