import constant

# region commands
start_menu = '/start'
# endregion commands
# add command -> add statement -> add command-statement -> statement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        # end command to constant

    }
    return switcher.get(command_present)
