python-labs
-----------

Dependencies
-----------

```shell
sudo yum groupinstall "Development tools"
sudo yum install python-devel expat-devel gdbm-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel xz-devel libevent-devel libffi-devel zlib-devel bzip2-devel gsl-devel atlas-devel freetype-devel libpng-devel blas-devel lapack-devel gcc-gfortran dvipng
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

Libraries
-----------

```shell
virtualenv -p /usr/local/bin/python2.7 dev
pip install -v httpie uwsgi iptools pycrypto redis pymysql glances boto cx_Freeze gevent Sphinx werkzeug numpy scipy matplotlib
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
