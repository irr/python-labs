#!/bin/bash
rm -rf devpy pypy
cp -r /opt/python/devpy . && cp -r /opt/python/pypy . && docker build -t webrest .
rm -rf devpy pypy
