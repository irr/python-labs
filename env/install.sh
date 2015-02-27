#!/bin/bash
mkdir -p /opt/python/github
cd /opt/python/github
git clone git@github.com:irr/high_performance_python.git
cd high_performance_python
git remote add upstream https://github.com/mynameisfiber/high_performance_python.git
git fetch upstream && git merge upstream/master && git push
cd ..
git clone git@github.com:irr/gevent-tutorial.git
cd gevent-tutorial
git remote add upstream https://github.com/sdiehl/gevent-tutorial.git
git fetch upstream && git merge upstream/master && git push
cd ..
git clone git@github.com:irr/python-guide.git
cd python-guide
git remote add upstream https://github.com/kennethreitz/python-guide.git
git fetch upstream && git merge upstream/master && git push
cd ..
git clone git@github.com:irr/awesome-python.git
cd awesome-python
git remote add upstream https://github.com/vinta/awesome-python.git
git fetch upstream && git merge upstream/master && git push
cd ~/gitf
ln -s /opt/python/github/awesome-python
ln -s /opt/python/github/gevent-tutorial
ln -s /opt/python/github/high_performance_python
ln -s /opt/python/github/python-guide
cd