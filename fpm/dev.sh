#!/bin/bash
VERSION=0.1
NAME=pydev
DEB=${NAME}_${VERSION}_amd64.deb
RPM=${NAME}-${VERSION}-1.x86_64.rpm
PACKAGE=${DEB}

echo "building ${PACKAGE}"

rm -rf ${PACKAGE}

if [[ "${PACKAGE}" =~ "rpm$" ]]
    then
        fpm -s dir -t rpm -n ${NAME} -v ${VERSION} --rpm-user irocha --rpm-group irocha \
            --prefix /home/irocha/dev \
            --description "virtualenv (dev)" -m "ivan.ribeiro@gmail.com" \
            -C $HOME/dev && \
        rpm -q -filesbypkg -p ${PACKAGE}
    else
        fpm -s dir -t deb -n ${NAME} -v ${VERSION} --deb-user irocha --deb-group irocha \
            --prefix /home/irocha/dev \
            --description "virtualenv (dev)" -m "ivan.ribeiro@gmail.com" \
            -C $HOME/dev && \
        dpkg -c ${PACKAGE}
fi
