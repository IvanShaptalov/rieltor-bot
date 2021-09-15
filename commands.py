import constant

# region commands
start_menu = '/start'
select_obj = 'обрати квартиру'

select_floor = '/select_floor'
select_flat = '/select flat'
select_flat_by_params = 'обрати квартиру по параметрам'
commercial_build = 'комерційні будівлі'
select_storeroom = 'кладові'


flat_detailed='/flat_detailed'
connect_to_manager='/manager'
# endregion commands
# add command -> add statement -> add command-statement -> statement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        select_obj: constant.Main.MENU,
        select_floor: constant.Main.FLOOR_SELECT,
        select_flat: constant.Main.FLAT_SELECT,
        select_flat_by_params: constant.Flat.BY_PARAMS,
        commercial_build: constant.Commercial.SELECT_COMMERCIAL,
        select_storeroom: constant.Storeroom.SELECT_STOREROOM,
        flat_detailed: constant.Flat.DETAILED,
        connect_to_manager: constant.Submit.CONNECT_TO_MANAGER,
        # end command to constant

    }
    return switcher.get(command_present)
