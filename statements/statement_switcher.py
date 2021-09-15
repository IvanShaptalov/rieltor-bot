import constant
from statements import main_menu
from statements.start_menu import start_menu


def select_statement_message(statement):
    from statements.comertial_build_dir.message_handler import comertial_build_module
    from statements.flat_by_param.message_handler import select_flat_by_params
    from statements.flat_statement.message_handler import select_flat_module
    from statements.floor_statement.message_handler import select_floor_module
    from statements.storeroom_dir.message_handler import storeroom_module
    from statements.flat_detailed_dir.message_handler import flat_detailed_module

    switcher = {
        # region message handlers

        constant.StartMenu.START_MENU: start_menu.handle_message,
        constant.Main.MENU: main_menu.handle_message,
        constant.Main.FLOOR_SELECT: select_floor_module.handle_message,
        constant.Main.FLAT_SELECT: select_flat_module.handle_message,
        constant.Flat.BY_PARAMS: select_flat_by_params.handle_message,
        constant.Commercial.SELECT_COMMERCIAL: comertial_build_module.handle_message,
        constant.Storeroom.SELECT_STOREROOM: storeroom_module.handle_message,
        constant.Flat.DETAILED: flat_detailed_module.handle_message,
        # endregion message handlers
    }

    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func


def select_statement_callback(statement):
    from statements.comertial_build_dir.callback_handler import comertial_build_module
    from statements.flat_by_param.callback_handler import select_flat_by_params
    from statements.flat_statement.callback_handler import select_flat_module
    from statements.floor_statement.callback_handler import select_floor_module
    from statements.storeroom_dir.callback_handler import storeroom_module
    from statements.flat_detailed_dir.callback_handler import flat_detailed_module
    from statements.sumbit_flat.callback_handler import handle_flat_module

    switcher = {
        # region callback handlers

        constant.Main.MENU: main_menu.handle_callback,
        constant.Main.FLOOR_SELECT: select_floor_module.handle_callback,
        constant.Main.FLAT_SELECT: select_flat_module.handle_callback,
        constant.Flat.BY_PARAMS: select_flat_by_params.handle_callback,
        constant.Commercial.SELECT_COMMERCIAL: comertial_build_module.handle_callback,
        constant.Storeroom.SELECT_STOREROOM: storeroom_module.handle_callback,
        constant.Flat.DETAILED: flat_detailed_module.handle_callback,
        constant.Submit.CONNECT_TO_MANAGER: handle_flat_module.handle_callback,
        # endregion callback handlers
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func
