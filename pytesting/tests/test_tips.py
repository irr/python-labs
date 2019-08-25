import functools
import numpy as np
import pytest
import random
import time

from app import WEBSITES

# set module mark
pytestmark = pytest.mark.tips

random.seed()

# pytest -vv -s -l -ra --tb=long --durations=10 (see pytest.ini)

# -vv: (verbose)
# -s: disable capturing output
# -l: show locals
# --tb: show all frames of failure tracebacks
# --durations=n: summary of the n longest running tests
# -ra: extra test summary

# DONT USE THIS! ONLY FOR DEMO/TEST
def delay(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        secs = round(random.uniform(0.3, 0.5), 2)
        params = {"args": list(*args), "kwargs": dict(**kwargs)}
        print(f"{func.__name__}[{params}] [wait={secs}]")
        time.sleep(secs)
        return func(*args, **kwargs)
    return wrapper_timer


@delay
def test_approx_dict():
    values = {'v1': 0.1 + 1.2, 'v2': 0.2 + 0.8}
    assert values == pytest.approx(dict(v1=1.3, v2=1.0))


@pytest.mark.ml
@delay
def test_approx_numpy():
    values = np.array([0.1, 0.2]) + np.array([1.2, 0.8])
    assert values == pytest.approx(np.array([1.3, 1.0]))


# test MUST fail!
@pytest.mark.xfail(strict=True)
@pytest.mark.ml
@delay
def test_numpy():
    values = np.array([0.1, 0.2]) + np.array([1.2, 0.8])
    assert values == np.array([1.3, 1.0])


@pytest.mark.parametrize(
    "data, result",
    [
        ((8, 4), 12.0),
        pytest.param(
            (1, 3), 4.0,
            marks=pytest.mark.ml,
            id="myparamtest"
            # call with: pytest -k myparamtest
        ),
    ],
)
@delay
def test_parametrize(data, result):
    values = sum(data)
    assert values == pytest.approx(result)


@delay
@pytest.mark.csv
def test_fixture_data(data_series):
    # call with: pytest -m csv
    assert len(data_series) == 4


@delay
@pytest.mark.csv
def test_fixture_mydata(my_data_series):
    # call with: pytest -m csv
    assert len(my_data_series) == 1


@pytest.mark.web
def test_web_handler(client):
    response = client.get("/")
    assert response.status_code == 200
    mapping = response.json
    for site in WEBSITES:
        assert mapping[site]["status"] == 200
