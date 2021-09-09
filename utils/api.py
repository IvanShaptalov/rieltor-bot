import datetime
from utils import db_util, json_util
import requests
from icecream import ic
from config_interpreter import host, protocol, api_key


def get_main_data_by_id(obj_id: int):
    now = datetime.datetime.now()
    main_link = f'{protocol}://{host}/api/v1/unit/object?hierarchy=1&id={obj_id}&api_key={api_key}'
    try:
        response = requests.get(main_link)
    except ConnectionError as e:
        ic('error while getting main object from site api')
        ic(type(e), e)
    else:
        return response.text or None
    print('seconds: ', (datetime.datetime.now() - now).seconds)


def save_all_data_to_db():
    data_list = []
    for id_ in range(1, 9):
        data = get_main_data_by_id(id_)
        if data:
            prepared_data = json_util.prepare_data_to_db(json_data=data)
            db_util.Snippets.save_data_to_db(prepared_data=prepared_data)
            ic(f'data from object # {id_} saved!')
        else:
            ic(f'data not loaded - object# {id_}')


if __name__ == '__main__':
    save_all_data_to_db()

