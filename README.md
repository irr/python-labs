python-labs
-----------

Dependencies
-----------

```shell
# Python 2
sudo apt-get install libatlas-dev libfreetype6-dev libpng12-dev \
                     libblas-dev liblapack-dev gfortran glances \
                     httpie python-crypto python-doc python-ipy \
                     python-setuptools python-gevent python-gevent-doc \
                     python-matplotlib python-matplotlib-doc python-nltk \
                     python-numpy python-numpy-doc python-pil python-pip \
                     python-redis python-requests python-scipy \
                     python-sklearn python-sklearn-doc python-sphinx \
                     python-virtualenv graphviz eclipse
# http://pydev.org/updates
# http://download.eclipse.org/egit/updates
# https://marketplace.eclipse.org/content/eclipse-moonrise-ui-theme

# Python 3
sudo apt-get install libatlas-dev libfreetype6-dev libpng12-dev \
                     libblas-dev liblapack-dev gfortran glances \
                     httpie python3-dev python3-doc python3-pip \
                     python-ipy python-pip python-virtualenv \
                     python-gevent python-gevent-doc graphviz
```

Libraries
-----------

```shell
pip install -v cython git+http://github.com/gevent/gevent.git#egg=gevent Flask aiohttp
pip install -v redis pymysql pycrypto iptools netaddr httpie glances pylint pycallgraph
pip install -v boto3 geopy python-geohash paramiko pyyaml sphinx sphinx_rtd_theme
pip install -v nltk numpy matplotlib scipy pandas scikit-learn
pip install -v gevent Flask # Python 2
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
