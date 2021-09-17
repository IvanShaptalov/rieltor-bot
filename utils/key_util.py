from telebot import types

import commands

inline_symbols = []


def create_reply_keyboard(*titles, is_resize: bool = True, row_width: int = 1, request_contact=None):
    """@:param args - button titles"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=is_resize, row_width=row_width)
    for title in titles[0]:
        button = types.KeyboardButton(title, request_contact=request_contact)
        markup.add(button)

    return markup


def create_inline_keyboard(switch_inline_query_current_chat=None, callback_data=False,
                           title_to_data=None, link=None):
    markup = types.InlineKeyboardMarkup()
    for dictionary in title_to_data:
        for title, data in dictionary.items():
            inline_button = types.InlineKeyboardButton(
                switch_inline_query_current_chat=switch_inline_query_current_chat,
                text=title,
                callback_data=data if callback_data else None,
                url=link)

            markup.add(inline_button, row_width=3)
    return markup


def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup


def create_request_markup(title, request_contact=None, request_location=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        types.KeyboardButton(text=title, request_contact=request_contact, request_location=request_location))
    return markup


class KeySnippets:
    main_menu_key = create_reply_keyboard([commands.select_obj, commands.select_flat_by_params, commands.select_storeroom, commands.commercial_build])