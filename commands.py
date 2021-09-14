import constant

# region commands
start_menu = '/start'
main_menu = '/choose_obj'


# endregion commands
# add command -> add statement -> add command-statement -> statement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        main_menu: constant.Main.MENU,
        # end command to constant

    }
    return switcher.get(command_present)
