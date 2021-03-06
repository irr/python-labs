#!/usr/bin/env python

# pip install numpy flask simplejson psutil

import logging
import os
import pickle
import psutil
import random
import simplejson as json
import uuid

import ctypes as c
import numpy as np
import multiprocessing as mp

from datetime import datetime
from flask import g, Flask, current_app, jsonify, request, abort


app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


N, M, D = int(100000000 / 10), 10, int(100000000 / 1000)
np_type_to_ctype = {
    np.float32: c.c_float,
    np.float64: c.c_double,
    np.bool: c.c_bool,
    np.uint8: c.c_ubyte,
    np.uint64: c.c_ulonglong
}


def _pmem():
    process = psutil.Process()
    mem = process.memory_info().rss / float(2 ** 20)
    memp = process.memory_percent()
    return (process.pid, mem, memp)


def pmem():
    pid, mem, memp = _pmem()
    print(f"main: pid={pid}, mem={mem}, percent={memp}")


@app.before_request
def before_request():
    g.start_time = datetime.now()
    g.request_id = str(uuid.uuid4())


@app.after_request
def after_request(response):
    dt = datetime.now() - g.start_time
    ms = str(round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0))
    response.headers['X-Profile'] = ms
    response.headers['X-Req'] = g.request_id
    return response


@app.route("/", methods=["GET"])
def base_handler():
    mp_arr = np.frombuffer(MP_ARRAY, dtype=np.float64, count=N * M)
    pmem()
    return jsonify({
        "array": {"id": id(mp_arr), "len": len(mp_arr)},
        "dict": {"id": id(current_app.mp_dict), "len": len(current_app.mp_dict)}
    })


def start(bind="0.0.0.0", port=6666, mp_dict=None):
    print(f"pid={os.getpid()} listener={bind}:{port}")
    with app.app_context():
        current_app.mp_dict = mp_dict
    app.run(host=bind, port=port, debug=False)


def start_all(count=None, bind="0.0.0.0", port=6666):
    for i in range(mp.cpu_count() if count is None else count):
        p = mp.Process(target=start, args=(bind, port + i, MP_DICT))
        p.start()
    return p


def load():
    global MP_ARRAY
    global MP_DICT

    if os.path.exists("nparray.dat"):
        print("loading numpy array...")
        with open('nparray.dat', 'rb') as k:
            arr = pickle.load(k)
        print("numpy array loaded")
    else:
        print("creating numpy array...")
        arr = np.arange(N * M)
        with open("nparray.dat", "wb") as f:
            pickle.dump(arr, f)

    MP_ARRAY = mp.RawArray(np_type_to_ctype[np.float64], arr.flat)

    manager = mp.Manager()
    if os.path.exists("mpdict.dat"):
        print("loading dict...")
        with open('mpdict.dat', 'rb') as k:
            d = pickle.load(k)
        print("dict loaded")
    else:
        print("creating huge dict...")
        d = { f"k{v}": v * 2 for v in range(D) }
        with open("mpdict.dat", "wb") as f:
            pickle.dump(d, f)

    MP_DICT = manager.dict(d)

    pmem()


if __name__ == "__main__":
    load()
    start_all().join()
