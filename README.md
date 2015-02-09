python-labs
-----------

Dependencies
-----------

```shell
sudo yum groupinstall "Development tools"
sudo yum install python-devel expat-devel gdbm-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel xz-devel libevent-devel libffi-devel zlib-devel bzip2-devel gsl-devel atlas-devel freetype-devel libpng-devel blas-devel lapack-devel gcc-gfortran dvipng graphviz-devel
```

```shell
wget http://python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar xfva Python-2.7.9.tgz
cd Python-2.7.9
./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j4
sudo make altinstall
sudo cp ~/python/env/python2.7.conf /etc/ld.so.conf.d/
sudo ldconfig

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
python2.7 ez_setup.py
easy_install-2.7 pip
pip2.7 install [packagename]
pip2.7 install --upgrade [packagename]
pip2.7 uninstall [packagename]
```

Libraries
-----------

```shell
virtualenv -p /usr/local/bin/python2.7 dev
pip install -v httpie uwsgi iptools pycrypto redis pymysql glances boto cx_Freeze pyinstaller gevent Sphinx werkzeug numpy scipy matplotlib
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
