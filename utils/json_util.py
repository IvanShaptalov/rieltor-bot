import json
from copy import copy

from icecream import ic


def prepare_data_to_db(json_data) -> dict:
    data = json.loads(json_data)
    assert isinstance(data, dict)
    key_list = ['data', 'objects', 0]
    object_name = try_get_from_dict(data, copy(key_list))
    key_list.append('houses')
    object_houses = try_get_from_dict(data, copy(key_list))
    # solved create flat decompiling
    house_list = []
    unique_flat_status = []
    for house in object_houses:
        # solved check this part, this is unstable
        assert isinstance(house, dict)
        name = try_get_from_dict(house, ['name'])
        house_id = try_get_from_dict(house, ['id'])
        house_sections = try_get_from_dict(house, ['sections'])
        section_list = []
        for section in house_sections:
            section_id = try_get_from_dict(section, ['id'])
            parking = try_get_from_dict(section, ['parking'])

            free_flats = []
            for raw_flat in try_get_from_dict(section, ['units']):

                flat_status = try_get_from_dict(raw_flat, ['status', 'name'])
                # solved check this condition
                if flat_status not in unique_flat_status:
                    unique_flat_status.append(flat_status)
                if (flat_status.lower() or "exception") == 'вільна':
                    price = try_get_from_dict(raw_flat, ['current_cost_set'])
                    price_m2 = try_get_from_dict(raw_flat, ['current_price_set'])
                    currency = try_get_from_dict(raw_flat, ['current_currency_set']) or try_get_from_dict(raw_flat, [
                        'company_default_currency'])
                    flat_id = try_get_from_dict(raw_flat, ['unit_id'])
                    rooms = try_get_from_dict(raw_flat, ['rooms'])
                    floor = try_get_from_dict(raw_flat, ['floor'])
                    area = try_get_from_dict(raw_flat, ['area_total'])
                    result_flat = {'price': price, 'flat_id': flat_id,
                                   'rooms': rooms, 'floor': floor,
                                   'area': area, 'section_id': section_id, 'price_m2': price_m2, 'currency': currency,
                                   'value_tuple': (price, flat_id, rooms, floor, area, section_id, price_m2, currency),
                                   'key_tuple': "price, flat_id, rooms, floor, area, section_id, price_m2, currency"}
                    free_flats.append(result_flat)
            if len(free_flats) >= 1:
                result_section = {"section": {'section_id': section_id, 'parking': parking,
                                              'house_id': house_id, 'free_flats': free_flats,
                                              'value_tuple': (section_id, parking, house_id),
                                              'key desc': "section_id, parking, house_id"}}
                section_list.append(result_section)
        object_house = {"house_obj": {'house_name': name, 'house_id': house_id,
                                      'sections': section_list,
                                      'value_tuple': (name, house_id),
                                      'key desc': "name, house_id"}}
        ic(unique_flat_status)
        return object_house

    return data


def try_get_from_dict(data: dict, key_list: list):
    if len(key_list) == 1:
        key = key_list[0]
        # noinspection PyBroadException
        try:
            return data[key]
        except:
            return None
    key = key_list.pop(0)

    try:
        new_data = data[key]
    except KeyError as e:
        print(f'key error on {key}')
    else:
        return try_get_from_dict(new_data, key_list)
