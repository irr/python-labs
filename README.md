python-labs
-----------

Dependencies
-----------

```shell
# Python 2.x/3.x
sudo yum groupinstall "Development tools"
sudo yum install python-devel expat-devel gdbm-devel zlib-devel \
                 bzip2-devel openssl-devel ncurses-devel sqlite-devel \
                 readline-devel xz-devel libev-devel libffi-devel \
                 zlib-devel bzip2-devel gsl-devel atlas-devel \
                 freetype-devel libpng-devel blas-devel tk-devel \
                 lapack-devel gcc-gfortran dvipng graphviz-devel

# http://pydev.org/updates
# http://download.eclipse.org/egit/updates

sudo mkdir -p /opt/python
sudo chown irocha: /opt/python
cd /opt/python
wget -c https://docs.python.org/2/archives/python-2.7.6-docs-html.tar.bz2
tar xfva python-2.7.6-docs-html.tar.bz2
wget -c https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
tar xfva Python-2.7.6.tar.xz
cd Python-2.7.6
./configure --prefix=/usr/local \
            --enable-unicode=ucs4 \
            --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j4
sudo make altinstall
sudo cp ~/python/env/python2.7.conf /etc/ld.so.conf.d/
sudo ldconfig

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
sudo /usr/local/bin/python2.7 ez_setup.py
sudo /usr/local/bin/easy_install-2.7 pip
sudo /usr/local/bin/pip2.7 install virtualenv

virtualenv -p /usr/local/bin/python2.7 dev
```

```shell
# Python 2.x
sudo apt-get install libatlas-dev libfreetype6-dev libpng12-dev \
                     libsqlite3-dev libmysqlclient-dev libzmq3-dev \
                     libblas-dev liblapack-dev gfortran glances \
                     geoip-bin geoip-database libgeoip-dev libev-dev \
                     httpie python-crypto python-doc python-ipy \
                     python-setuptools python-gevent python-gevent-doc \
                     python-matplotlib python-matplotlib-doc python-nltk \
                     python-numpy python-numpy-doc python-pil python-pip \
                     python-redis python-requests python-scipy \
                     python-sklearn python-sklearn-doc python-sphinx \
                     python-virtualenv graphviz eclipse

# Python 3.x
sudo apt-get install libatlas-dev libfreetype6-dev libpng12-dev \
                     libsqlite3-dev libmysqlclient-dev libzmq3-dev \
                     geoip-bin geoip-database libgeoip-dev libev-dev \
                     libblas-dev liblapack-dev gfortran glances \
                     httpie python3-dev python3-doc python3-pip \
                     python-ipy python-pip python-virtualenv \
                     python-gevent python-gevent-doc graphviz
```

Libraries
-----------

```shell
# Python 3.x
pip install -v aiohttp aioredis aiomysql geopy python-geohash pyyaml
pip install -v pycrypto iptools beautifulsoup4 nltk textblob
pip install -v httpie glances sphinx sphinx_rtd_theme
pip install -v cython git+http://github.com/gevent/gevent.git#egg=gevent

# Python 2.7
pip install -v Flask gevent
pip install -v redis pymysql pycrypto iptools netaddr beautifulsoup4
pip install -v cassandra-driver lz4
pip install -v httpie glances pycallgraph
pip install -v boto3 geopy python-geohash paramiko pyyaml sphinx sphinx_rtd_theme
pip install -v nltk textblob numpy matplotlib scipy pandas scikit-learn
```

```python
import nltk, textblob.download_corpora
nltk.download()
textblob.download_corpora.main()
```

```shell
cd /opt/python
wget http://nginx.org/download/nginx-1.9.4.tar.gz
tar xfva nginx-1.9.4.tar.gz
cd nginx-1.9.4
./configure --with-http_ssl_module \
            --prefix=/opt/python/nginx
make -j4
make install
cd /usr/sbin
sudo ln -s /opt/python/nginx/sbin/nginx
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
