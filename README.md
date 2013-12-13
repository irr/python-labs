python-labs
-----------

Dependencies
-----------

```shell
yum groupinstall "Development tools"
yum install expat-devel gdbm-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel xz-devel libevent-devel libffi-devel compat-gdbm-devel zlib-devel tkimg-devel bzip2-devel
```

```shell
wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar xfva Python-2.7.6.tgz
cd Python-2.7.6
./configure --enable-shared --prefix=/usr/local
make -j4
make altinstall
```

Libraries
-----------

```shell
pip install -v httpie gevent iptools pycrypto redis umysql tornado tornado-redis torndb MySQL-python psutil glances pyinstaller
```

```shell
git clone https://github.com/defnull/bottle.git
cd bootle
python setup.py install
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
