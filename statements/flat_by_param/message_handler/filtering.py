import re

import telebot
from icecream import ic

import commands
from statements import useful_methods
from utils import db_util, key_util
from statements.flat_by_param.callback_handler import paginator
from statements.flat_detailed_dir.callback_handler import flat_detailed_module

def is_flat_id(message: telebot.types.Message):
    """function to check if message have flat id """
    if "/info" in message.text:
        result = re.findall(r'\d+', message.text)
        if len(result) == 1:
            if isinstance(result[0], str) and result[0].isdigit():
                data = int(result[0])
                flat = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                                 identifier=db_util.FreeFlat.flat_id,
                                                                 value=data)
                if isinstance(flat, db_util.FreeFlat):
                    return data


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    useful_methods.change_statement(statement=commands.filtering, message=message, chat_id=chat_id)
    result = check_data(input_data=message.text)
    section = get_section(chat_id)
    # solved change statement to select flat
    flat_data = is_flat_id(message)
    if isinstance(flat_data, int):
        useful_methods.change_statement(statement=commands.flat_detailed, chat_id=chat_id, message=message)
        call = telebot.types.CallbackQuery(data=flat_data,
                                           id=1,
                                           chat_instance=None,
                                           from_user=message.from_user,
                                           message=message)
        flat_detailed_module.handle_callback(call=call, bot=bot)
        return
        # go to detailed message
    if isinstance(section, db_util.UserChosenField):
        if isinstance(result, str):
            bot.send_message(chat_id=chat_id,
                             text=result + "\nспробуйте ввести дані знову")
        else:
            t = 1000
            dictionary = result[1]
            room_count = dictionary['room_count']
            price_for_m2_min = dictionary['price_for_m2'][0] * t
            price_for_m2_max = dictionary['price_for_m2'][1] * t
            total_area_min = dictionary['total_area'][0]
            total_area_max = dictionary['total_area'][1]
            # solved define section
            print("info: ", result[1])
            house_id = section.section_id
            ic(house_id)
            # solved write tests to this function
            flats = filter_flats(house_id=house_id,
                                 room_count=room_count,
                                 total_area_min=total_area_min,
                                 total_area_max=total_area_max,
                                 price_for_m2_min=price_for_m2_min,
                                 price_for_m2_max=price_for_m2_max)
            ic(len(flats))
            if flats:
                print(
                    [f"flat rooms: {flat.rooms} flat area: {flat.total_area} flat_price for m2 {flat.price_m2}" for flat
                     in
                     flats])
                # solved send flat_list by param
                bot.send_message(chat_id=chat_id,
                                 text="Ви обрали квартири з наступними характеристиками:\n"
                                      f"Кількість кімнат : {room_count}\n"
                                      f"Площа : {total_area_min} - {total_area_max} м2\n"
                                      f"Ціна за м2 : {price_for_m2_min} - {price_for_m2_max}\n"
                                      f"Квартир знайдено: {len(flats)}",
                                 reply_markup=key_util.KeySnippets.main_menu_key)
                # solved save association in database
                db_util.drop_chat(chat_id=chat_id)
                db_util.save_flats_to_chat(chat_id=chat_id, flats=flats)
                # solved send pagination
                paginator.send_flats(message=message, bot=bot)
    else:
        bot.send_message(chat_id=chat_id,
                         text='Данна секція не існує',
                         reply_markup=key_util.KeySnippets.main_menu_key)


# solved create test to this moment
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


def get_section(chat_id):
    choice = db_util.get_from_db_multiple_filter(table_class=db_util.UserChosenField,
                                                 identifier_to_value=[db_util.UserChosenField.chat_id == chat_id],
                                                 get_type='one')
    return choice


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


def filter_flats(house_id,
                 room_count,
                 total_area_min,
                 total_area_max,
                 price_for_m2_min,
                 price_for_m2_max):
    ident_value = [db_util.FreeFlat.section.has(house_obj_id=house_id),
                   db_util.FreeFlat.rooms == room_count,
                   db_util.FreeFlat.total_area >= total_area_min,
                   db_util.FreeFlat.total_area <= total_area_max,
                   db_util.FreeFlat.price_m2 >= price_for_m2_min,
                   db_util.FreeFlat.price_m2 <= price_for_m2_max]
    flats = db_util.get_from_db_multiple_filter(table_class=db_util.FreeFlat,
                                                get_type='many',
                                                identifier_to_value=ident_value)
    return flats
