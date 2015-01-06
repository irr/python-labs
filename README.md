python-labs
-----------

Dependencies
-----------

```shell
yum groupinstall "Development tools"
yum install expat-devel gdbm-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel xz-devel libevent-devel libffi-devel compat-gdbm-devel zlib-devel tkimg-devel bzip2-devel gsl-devel
```

```shell
wget http://python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar xfva Python-2.7.9.tgz
cd Python-2.7.9
./configure --enable-shared --prefix=/usr/local
make -j4
sudo make altinstall
sudo cp ~/python/env/python2.7.conf /etc/ld.so.conf.d/
sudo ldconfig
```

```shell
wget http://python.org/ftp/python/3.4.2/Python-3.4.2.tgz
tar xfva Python-3.4.2.tgz
cd Python-3.4.2
./configure --enable-shared --prefix=/usr/local
make -j4
sudo make altinstall

wget --no-check-certificate https://pypi.python.org/packages/source/d/distribute/distribute-0.7.3.zip
unzip distribute-0.7.3.zip
cd distribute-0.7.3

su -c "python3.4 setup.py install"
su -c "easy_install-3.4 virtualenv"
```

Libraries
-----------

```shell
virtualenv -p /usr/local/bin/python2.7 dev
virtualenv-3.4 -p /usr/local/bin/python3.4 dev3
pip install -v httpie uwsgi iptools pycrypto redis pymysql glances boto cx_Freeze werkzeug
```

Copyright and License
---------------------
Copyright 2012 Ivan Ribeiro Rocha

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[Python]: http://python.org/
