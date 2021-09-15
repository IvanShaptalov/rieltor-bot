import pytest
from icecream import ic


# py.test -m call_data -v

@pytest.mark.config
def test_config_valid():
    try:
        import config_interpreter
    except KeyError as e:
        assert False, "config valid failed"
    ic('test_config_valid - ok')


def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:
        requests.get(google)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'


def test_main_data_from_api():
    from utils import api
    result = api.get_main_data_by_id(8)
    assert result is not None, "result in None"


