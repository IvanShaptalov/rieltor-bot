import json
from copy import copy
from typing import List


def prepare_data_to_db(json_data):
    data = json.loads(json_data)
    assert isinstance(data, dict)
    key_list = ['data', 'objects', 0]
    object_name = try_get_from_dict(data, copy(key_list))
    key_list.append('houses')
    object_houses = try_get_from_dict(data, copy(key_list))
    # todonow
    house_list = []
    for house in object_houses:
        assert isinstance(house, dict)
        name = try_get_from_dict(house, ['name'])
        house_id = try_get_from_dict(house, ['id'])
        house_sections = try_get_from_dict(house, ['sections'])
        ...
    return data


def try_get_from_dict(data: dict, key_list: list):
    if len(key_list) == 1:
        key = key_list[0]
        return data[key]
    key = key_list.pop(0)

    try:
        new_data = data[key]
    except KeyError as e:
        print(f'key error on {key}')
    else:
        return try_get_from_dict(new_data, key_list)
