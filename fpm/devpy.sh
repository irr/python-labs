#!/bin/bash
VERSION=0.1
NAME=pydev
DEB=${NAME}_${VERSION}_amd64.deb
RPM=${NAME}-${VERSION}-1.x86_64.rpm
PACKAGE=${DEB}
DIST=devpy

echo "building ${PACKAGE}"

rm -rf ${PACKAGE}

if [[ "${PACKAGE}" =~ "rpm$" ]]
    then
        fpm -s dir -t rpm -n ${NAME} -v ${VERSION} --rpm-user root --rpm-group root \
            --prefix /opt/python/pypy \
            --description "virtualenv (${DIST})" -m "ivan.ribeiro@gmail.com" \
            -C /opt/python/pypy && \
        rpm -q -filesbypkg -p ${PACKAGE}
    else
        fpm -s dir -t deb -n ${NAME} -v ${VERSION} --deb-user root --deb-group root \
            --prefix /opt/python/pypy \
            --description "virtualenv (${DIST})" -m "ivan.ribeiro@gmail.com" \
            -C /opt/python/pypy && \
        dpkg -c ${PACKAGE}
fi
