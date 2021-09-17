import pytest

from statements.flat_detailed_dir.callback_handler import flat_detailed_module
from statements.flat_statement.callback_handler import select_flat_module
from utils import db_util


@pytest.mark.call_data
def test_get_object():
    # solved get valid
    from statements import main_menu
    valid_key = 1
    result = main_menu.get_house_obj(valid_key)
    assert isinstance(result, db_util.HouseObj), "db not have valid house "
    invalid_key = 'aboba'
    result = main_menu.get_house_obj(invalid_key)
    assert result is None, f"invalid key :{invalid_key} raise error and result - :{result} while try get house"


@pytest.mark.call_data
def test_get_section():
    from statements import main_menu
    valid_key = 1
    result = main_menu.get_sections(valid_key)
    assert isinstance(result, list), "db not have valid sections in house "
    invalid_key = 'aboba'
    result = main_menu.get_house_obj(invalid_key)
    assert result is None, f"invalid key :{invalid_key} raise error and result - :{result} while try get sections in house"


@pytest.mark.call_data
def test_get_floor():
    valid_key = 82
    from statements.floor_statement.callback_handler import select_floor_module
    result = select_floor_module.get_from_db_prepare_data(valid_key)
    assert isinstance(result, list), "db not have valid floor with flats in this section"
    assert isinstance(result[0], dict), "db not have valid dict floor in list"
    invalid_key = 'aboba'
    result = select_floor_module.get_from_db_prepare_data(invalid_key)
    assert result is None, f"invalid key :{invalid_key} raise error and result - :{result} while try get sections in house"


@pytest.mark.call_data
def test_get_flats():
    valid_key = '1-1'
    result = select_flat_module.get_from_db_prepare_data(valid_key)
    assert isinstance(result, list), "it is not flat list"
    assert isinstance(result[0], dict), "it is not prepared dictionary"
    invalid_keys = ['mo bamba', 'mo-bamba', '', 'mo-1']
    for invalid_key in invalid_keys:
        result = select_flat_module.get_from_db_prepare_data(invalid_key)
        assert result is None, f"return not None from invalid key {invalid_key}"


@pytest.mark.call_data
def test_get_one_flat():
    valid_key = 102202
    result = flat_detailed_module.get_from_db_prepare_data(valid_key)
    assert isinstance(result, tuple), "db not have valid flats on this key "
    invalid_key = 'aboba'
    result = flat_detailed_module.get_from_db_prepare_data(invalid_key)
    assert result is None, f"invalid key :{invalid_key} raise error and result - :{result} while try get flat"


@pytest.mark.call_data
def test_get_flat_by_params(flat_filter_params):
    ...  # todonext after pagination
