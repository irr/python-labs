import csv
import pytest

@pytest.fixture
def data_series():
	with open("tests/data.csv", "r", newline="") as file:
		return list(csv.reader(file, delimiter=","))


# fixture composed by another fixture
@pytest.fixture
def my_data_series(data_series):
	return [x for x in data_series if x[0] == "twitter"]


@pytest.fixture
def app():
	from app import application
	return application
