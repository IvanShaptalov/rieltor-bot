import telebot

import commands
from statements import useful_methods
from statements.main_menu import get_house_obj
from utils import db_util, key_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call and call.data and call.message:
        section_id = call.data
        chat_id = useful_methods.id_from_message(call.message)
        house = get_house_obj(call_id=section_id)
        save_section(section_id=section_id, chat_id=chat_id)
        useful_methods.change_statement(statement=commands.filtering, chat_id=chat_id, message=call.message)
        useful_methods.try_delete_message(message=call.message, bot=bot)
        example = '1,10-60,10-100'
        markup = key_util.create_reply_keyboard([example])
        bot.send_message(chat_id=chat_id,
                         text='Введіть пункти фільтрації наступним чином\n'
                              '(тільки цифри та коми, без слів в дужках):\n'
                              '(кількість кімнат)5\n'
                              '(ціна за м2 в тис.)10-20\n'
                              '(загальна площа)100-200\n'
                              'приклад: (натисніть на кнопку або відправте повідомлення)\n'
                              f'{example}',
                         reply_markup=markup)


def save_section(section_id, chat_id):
    print('write section')
    db_util.write_obj_to_table(table_class=db_util.UserChosenField,
                               identifier=db_util.UserChosenField.chat_id,
                               value=chat_id,
                               chat_id=chat_id,
                               section_id=section_id)
    print('saved')
    # solved create filtering flats using house > rooms, price, area

