import pytest
from icecream import ic

# py.test -m call_data -v
from statements.flat_by_param.message_handler import filtering


@pytest.mark.config
def test_config_valid():
    try:
        import config_interpreter
    except KeyError as e:
        assert False, "config valid failed"
    ic('test_config_valid - ok')


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:
        requests.get(google)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'


@pytest.mark.internet
def test_main_data_from_api():
    from utils import api
    result = api.get_main_data_by_id(8)
    assert result is not None, "result in None"


@pytest.mark.filtering
def test_filter_flat(invalid_filter_params, valid_filter_params):
    for param in invalid_filter_params:
        assert isinstance(filtering.check_data(param), str), f"filter pass bad arguments: {param}"
    for param in valid_filter_params:
        assert isinstance(filtering.check_data(param), tuple), f"filter not pass valid param: {param}"
