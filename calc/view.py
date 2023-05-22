import logging

from . import messages as msg
from . import model

logger = logging.getLogger(__name__)


def print_separator_line():
    print()


def print_message(message):
    print(message.strip())


def get_user_input(message=None):
    if message is not None:
        print_message(message)
    return input().strip()


# main menu
def get_menu_option_main():
    return get_user_input(msg.MENU_MAIN + msg.INFO_ENTER_OPTION)


# crud menu
def get_menu_option_crud():
    return get_user_input(msg.MENU_CRUD + msg.INFO_ENTER_OPTION)


# top_ten menu
def get_menu_option_top_ten():
    return get_user_input(msg.MENU_TOP_TEN + msg.INFO_ENTER_OPTION)


# database initialization
def init_db(force=False):
    if model.init_db(force):
        print_message(msg.INFO_DB_CREATED)


# exit
def print_exit_message():
    print_message(msg.INFO_GOODBYE)


# print not implemented message
def print_not_implented():
    print_message(msg.ERROR_NOT_IMPLEMENTED)


# print wrong option message
def print_invalid_menu_option_error():
    print_message(msg.ERROR_INVALID_OPTION)


# unhandled command
def print_unhandled_command_message(*unhandled_command):
    print("ERROR: unhandled_command: ", unhandled_command)
