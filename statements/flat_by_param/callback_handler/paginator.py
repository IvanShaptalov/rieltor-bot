from telegram_bot_pagination import InlineKeyboardPaginator

import config_interpreter
from statements import useful_methods
from utils import db_util


def handle_callback(call, bot):
    page = int(call.data.split('#')[1])

    useful_methods.try_delete_message(message=call.message, bot=bot)

    send_page(call.message, bot=bot, page=page)


def send_flats(message, bot):
    send_page(message, bot=bot)


# send paginator first
def get_flats_from_db(chat_id):
    return db_util.get_all_flats_from_associate_table(chat_id)


def prepare_flat(flat):
    if isinstance(flat, db_util.FreeFlat):
        section = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseSection,
                                                            identifier=db_util.HouseSection.section_id,
                                                            value=flat.section_id)
        if isinstance(section, db_util.HouseSection):
            house = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseObj,
                                                              identifier=db_util.HouseObj.house_id,
                                                              value=section.house_obj_id)
            if isinstance(house, db_util.HouseObj):
                parking = "Є паркінг\n" if int(section.parking) == 1 else ""
                text = f"\nБудинок: {house.house_name} секція - {section.section_id}\nЦіна {flat.price} {flat.currency}\n{parking}" \
                       f"Детальніше:\n/info{flat.flat_id}\n"
                return text


def prepare_flats(flat_list, page, flats_by_page):
    start_element = (page-1) * flats_by_page
    check = start_element + flats_by_page
    last_element = check if check <= len(flat_list) else -1
    flats_to_filter = flat_list[start_element:last_element]
    result_flats = list(map(prepare_flat, flats_to_filter))
    return result_flats


def send_page(message, bot, page=1):
    chat_id = message.chat.id
    flat_list = get_flats_from_db(chat_id)
    if flat_list is None:
        return
    # todonow prepare using page
    flats_by_page = 4
    result_flats = prepare_flats(flat_list, page, flats_by_page)
    last = 1 if int(len(flat_list) % flats_by_page) != 0 else 0
    flat_pages = int(len(flat_list) // flats_by_page) + last
    paginator = InlineKeyboardPaginator(
        flat_pages,
        current_page=page,
        data_pattern='flats#{page}'
    )
    text = "".join(result_flats)
    text = "." if text == "" else text
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
