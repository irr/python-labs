python-labs
-----------

Dependencies
-----------

```shell
yum groupinstall "Development tools"
yum install expat-devel gdbm-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel xz-devel libevent-devel libffi-devel compat-gdbm-devel zlib-devel tkimg-devel bzip2-devel
```

```shell
./configure --prefix=/opt/python/stackless
make -j4
make install
virtualenv --no-site-packages --distribute -p /opt/python/stackless/bin/python dev7
```

Libraries
-----------

```shell
pip install -v httpie gevent iptools pycrypto redis umysql bottle psutil glances
```

* [Stackless]: Stackless Python is an enhanced version of the Python programming language. It allows programmers to reap the benefits of thread-based programming without the performance and complexity problems associated with conventional threads. The microthreads that Stackless adds to Python are a cheap and lightweight convenience which can if used properly, give several benefits

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

[Stackless]: http://www.stackless.com/
[Python]: http://python.org/
