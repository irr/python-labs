#!/bin/bash

# ls -alF /opt/python/pypy
# total 16
# drwxrwxr-x 4 irocha irocha 4096 Feb 29 13:54 ./
# drwxr-xr-x 6 irocha irocha 4096 Feb 29 13:53 ../
# drwxrwxr-x 6 irocha irocha 4096 Feb 29 13:54 devpy/
# drwxr-xr-x 7 irocha irocha 4096 Nov 18 09:45 pypy-4.0.1-linux64/

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
