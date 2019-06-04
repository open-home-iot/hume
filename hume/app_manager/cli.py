OPTION_STATUS = 1
OPTION_SHUTDOWN = 2

MENU_OPTIONS = {
    OPTION_STATUS: 'Show status',
    OPTION_SHUTDOWN: 'Shutdown'
}

RUNNING = True


def menu():
    print("*****************")
    print("Select an option:")
    print("*****************")

    for key, option in MENU_OPTIONS.items():
        print(key, option)


def check_input(inp):
    return inp in MENU_OPTIONS.keys()


def await_option(app_manager):
    inp = int(input())
    if check_input(inp):
        perform_action(inp, app_manager)
    else:
        print("That option does not exist")


def perform_action(option, app_manager):
    if option == OPTION_STATUS:
        print("ASK IF SPECIFIC APPLICATION")
    elif option == OPTION_SHUTDOWN:
        app_manager.stop()
        global RUNNING
        RUNNING = False
    else:
        print("There is no action for that")


def start_cli(app_manager):
    while RUNNING:
        menu()
        await_option(app_manager)
