import logging
import sys

from . import view, model

logger = logging.getLogger(__name__)


def controller(command):
    logger.debug(str(command))
    match command:
        # main menu
        case ["menu", "main"]:
            option = view.get_menu_option_main()
            next_command = ["menu_option", "main", option]
        case ["menu_option", "main", "0"]:
            # 0. Exit
            next_command = ["one_off", "exit"]
        case ["menu_option", "main", "1"]:
            # 1 CRUD operations
            next_command = ["menu", "crud"]
        case ["menu_option", "main", "2"]:
            # 2 Show top ten companies by criteria
            next_command = ["menu", "top_ten"]
        case ["menu_option", "main", _]:
            # invalid option
            view.print_invalid_menu_option_error()
            next_command = ["menu", "main"]

        # crud menu
        case ["menu", "crud"]:
            option = view.get_menu_option_crud()
            next_command = ["menu_option", "crud", option]
        case ["menu_option", "crud", "0"]:
            # 0. back to main menu
            next_command = ["menu", "main"]
        case ["menu_option", "crud", "1"]:
            # 1 Create a company
            view.company_create()
            next_command = ["menu", "main"]
        case ["menu_option", "crud", "2"]:
            # 2 Read a company - select company
            company = view.select_company()
            next_command = ["crud", "read", company]
        case ["menu_option", "crud", "3"]:
            # 3 Update a company - select company
            company = view.select_company()
            next_command = ["crud", "update", company]
        case ["menu_option", "crud", "4"]:
            # 4 Delete a company - select company
            company = view.select_company()
            next_command = ["crud", "delete", company]
        case ["menu_option", "crud", "5"]:
            # 5 List all companies
            view.company_list_all()
            next_command = ["menu", "main"]
        case ["menu_option", "crud", _]:
            # invalid option
            view.print_invalid_menu_option_error()
            next_command = ["menu", "crud"]

        # crud company dependent executors
        case ["crud", _, None]:
            # handle no company has been found situation
            view.print_company_not_found_error()
            next_command = ["menu", "main"]
        case ["crud", "read", company]:
            view.company_read(company)
            next_command = ["menu", "main"]
        case ["crud", "update", company]:
            view.company_update(company)
            next_command = ["menu", "main"]
        case ["crud", "delete", company]:
            view.company_delete(company)
            next_command = ["menu", "main"]

        # top_ten menu
        case ["menu", "top_ten"]:
            option = view.get_menu_option_top_ten()
            next_command = ["menu_option", "top_ten", option]
        case ["menu_option", "top_ten", "0"]:
            # 0. back to main menu
            next_command = ["menu", "main"]
        case ["menu_option", "top_ten", "1"]:
            # 1 List by ND/EBITDA
            view.print_not_implented()
            next_command = ["menu", "main"]
        case ["menu_option", "top_ten", "2"]:
            # 2 List by ROE
            view.print_not_implented()
            next_command = ["menu", "main"]
        case ["menu_option", "top_ten", "3"]:
            # 3 List by ROA
            view.print_not_implented()
            next_command = ["menu", "main"]
        case ["menu_option", "top_ten", _]:
            # invalid option
            view.print_invalid_menu_option_error()
            next_command = ["menu", "top_ten"]

        # === one_off commands ===

        # welcome at program start
        case ["one_off", "welcome"]:
            view.print_welcome_message()

        # database initialization
        case ["one_off", "init_db", force]:
            view.init_db(force)

        # exit program
        case ["one_off", "exit"]:
            view.print_exit_message()
            sys.exit()

        # catch all for unhandled commands
        case [*unhandled_command]:
            view.print_unhandled_command_message(unhandled_command)
            next_command = ["menu", "main"]

    try:
        return next_command
    except UnboundLocalError:
        return None
