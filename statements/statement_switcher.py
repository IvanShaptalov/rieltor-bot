import constant
from statements import main_menu
from statements.start_menu import start_menu


# todonow create bot statements
def select_statement_message(statement):
    switcher = {
        # region message handlers
        constant.StartMenu.START_MENU: start_menu.handle_message,
        constant.Main.MENU: main_menu.handle_message,
        # endregion message handlers
    }

    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func


def select_statement_callback(statement):
    switcher = {
        # region callback handlers

        constant.Main.MENU: main_menu.handle_callback,
        # endregion callback handlers
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func
