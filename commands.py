import constant

# region commands
start_menu = '/start'
main_menu = '/choose_obj'

select_floor = '/select_floor'
select_flat = '/select_flat'
select_flat_by_params = '/flat_by_params'
commercial_build = '/commercial_build'
select_storeroom = '/storeroom'


# endregion commands
# add command -> add statement -> add command-statement -> statement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        main_menu: constant.Main.MENU,
        select_floor: constant.Main.FLOOR_SELECT,
        select_flat: constant.Main.FLAT_SELECT,
        select_flat_by_params: constant.Flat.BY_PARAMS,
        commercial_build: constant.Comertial.SELECT_COMERTIAL,
        select_storeroom: constant.Storeroom.SELECT_STOREROOM,
        # end command to constant

    }
    return switcher.get(command_present)
