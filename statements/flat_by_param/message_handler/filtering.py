import telebot

import commands
from statements import useful_methods
from statements.main_menu import get_house_obj
from utils import db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    useful_methods.change_statement(statement=commands.filtering, message=message, chat_id=chat_id)
    result = check_data(input_data=message.text)
    if isinstance(result, str):
        bot.send_message(chat_id=chat_id,
                         text=result + "\nспробуйте ввести дані знову")
    else:
        dictionary = result[1]
        room_count = dictionary['room_count']
        price_for_m2_min = dictionary['price_for_m2'][0]
        price_for_m2_max = dictionary['price_for_m2'][1]
        total_area_min = dictionary['total_area'][0]
        total_area_max = dictionary['total_area'][1]
        # todonow define section

        ident_value = [db_util.FreeFlat.section_id == 1,
                       db_util.FreeFlat.rooms == room_count,
                       db_util.FreeFlat.total_area >= total_area_min,
                       db_util.FreeFlat.total_area <= total_area_max,
                       db_util.FreeFlat.price_m2 >= price_for_m2_min,
                       db_util.FreeFlat.price_m2 <= price_for_m2_max]
        flats = db_util.get_from_db_multiple_filter(table_class=db_util.FreeFlat,
                                                    get_type='many',
                                                    identifier_to_value=ident_value)
        print(len(flats))
        # todonow send flat_list by param
        print('all ok start filter and get flats')
        bot.send_message(chat_id=chat_id,
                         text=f"все ок дані: {result}")


# todonext create test to this moment
def check_data(input_data):
    arr = input_data.split(',')
    if len(arr) == 3:
        room_count = arr[0]
        price_for_m2 = arr[1]
        total_area = arr[2]
        # check first parameter
        room_count_result = check_room_count(room_count)
        if not isinstance(room_count_result, int):
            return room_count_result
        price_for_m2_result = check_bound_correct(bound_on_str=price_for_m2,
                                                  error_m1="Ви не правильно заповнили поле ціна за м2.",
                                                  error_m2="Ціна за м2 некоректна!")
        if not isinstance(price_for_m2_result, tuple):
            return price_for_m2_result
        total_area_result = check_bound_correct(bound_on_str=total_area,
                                                error_m1="Ви не правильно заповнили поле загальна площа.",
                                                error_m2="Площа некоректна!")
        if not isinstance(total_area_result, tuple):
            return total_area_result
        return ('data_is_valid', {'room_count': room_count_result,
                                  'price_for_m2': price_for_m2_result,
                                  'total_area': total_area_result})
    else:
        return "Ви ввели не всі дані"


def check_bound_correct(bound_on_str: str, error_m1, error_m2):
    if not len(bound_on_str.split('-')) == 2:
        return error_m1
    else:
        arr = bound_on_str.split('-')
        el1 = arr[0].replace(' ', '', 100)
        el2 = arr[1].replace(' ', '', 100)
        if not el1.isdigit() or not el2.isdigit():
            return "Всі параметри мають вводитися цифрами"
        num1 = int(el1)
        num2 = int(el2)
        if num1 < 0 or num2 < 0:
            return error_m2
        if num1 > num2:
            num2, num1 = num1, num2
        return num1, num2


def check_room_count(room_count: str):
    room_count = room_count.replace(' ', '')
    if not room_count.isdigit():
        return "Кількість кімнат має вводитися цифрою."
    else:
        if int(room_count) < 0 or int(room_count) > 6:
            return "Кількість кімнат має бути від 0 до 6"
    return int(room_count)
