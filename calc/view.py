from itertools import count
import logging

from . import messages as msg
from .misc import FIELD_VIEW_META, UPDATE_FIELDS, STATISTICS
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


def company_create():
    company_data = {}
    for field, view_meta in FIELD_VIEW_META.items():
        company_data[field] = get_user_input(
            msg.PROMPT_ENTER_DATA.substitute(
                label=view_meta["label"], example=view_meta["example"]
            )
        )
    model.company_create(company_data)
    print_message(msg.INFO_COMPANY_CREATED)


def select_company():
    name = get_user_input(msg.PROMPT_ENTER_COMPANY_NAME)
    companies = model.companies_by_name(name)
    if companies is None:
        return None
    companies_with_index = dict(zip(
        (str(index) for index in count()),
        companies
    ))
    for index, company in companies_with_index.items():
        print(index, company['name'])
    # index = get_user_input(msg.PROMPT_ENTER_COMPANY_NUMBER)
    index = input(msg.PROMPT_ENTER_COMPANY_NUMBER)
    while index not in companies_with_index.keys():
        index = get_user_input(msg.ERROR_INVALID_OPTION)
    return companies_with_index[index]


def company_read(company_data):
    company_data = model.company_read(company_data)
    print_message(msg.INFO_COMPANY_READ_HEADER.substitute(
        ticker=company_data['ticker'], name=company_data['name']
    ))
    for stat_id, stat_function in STATISTICS.items():
        stat_value = stat_function(company_data)
        stat_value = (f"{round(stat_value, 2)}"
                      if stat_value is not None else None)
        print_message(msg.INFO_COMPANY_READ_STATISTIC.substitute(
            stat_id=stat_id, stat_value=stat_value))


def company_update(company_data):
    for field in UPDATE_FIELDS:
        view_meta = FIELD_VIEW_META[field]
        company_data[field] = get_user_input(
            msg.PROMPT_ENTER_DATA.substitute(
                label=view_meta["label"], example=view_meta["example"]
            )
        )
    model.company_update(company_data)
    print_message(msg.INFO_COMPANY_UPDATED)


def company_delete(company_data):
    model.company_delete(company_data)
    print_message(msg.INFO_COMPANY_DELETED)


def company_list_all():
    print_message(msg.INFO_COMPANY_LIST)
    for company_data in model.companies_get_all():
        print_message(msg.INFO_COMPANY_LIST_ENTRY.substitute(
            ticker=company_data['ticker'], name=company_data['name'],
            sector=company_data['sector']
        ))


# top_ten menu
def get_menu_option_top_ten():
    return get_user_input(msg.MENU_TOP_TEN + msg.INFO_ENTER_OPTION)


def print_top_ten(stat_id):
    all_data = model.get_all_data()
    stat_function = STATISTICS[stat_id]
    statistic_data = []
    for company_data in all_data:
        try:
            value = str(round(stat_function(company_data), 2))
        except TypeError:
            continue
        statistic_data.append((company_data["ticker"], value))
    statistic_data.sort(key=lambda stat_info: stat_info[1], reverse=True)
    print_message(msg.INFO_COMPANY_TOP_TEN_HEADER.substitute(stat_id=stat_id))
    for ticker, stat_value in statistic_data[:10]:
        print_message(msg.INFO_COMPANY_TOP_TEN_ENTRY.substitute(
            ticker=ticker, stat_value=stat_value))


# database initialization
def init_db(force=False):
    if model.init_db(force):
        # print_message(msg.INFO_DB_CREATED)
        pass


# welcome at program start
def print_welcome_message():
    print_message(msg.INFO_WELCOME)


# exit
def print_exit_message():
    print_message(msg.INFO_GOODBYE)


# print company not found message
def print_company_not_found_error():
    print_message(msg.ERROR_COMPANY_NOT_FOUND)


# print not implemented message
def print_not_implented():
    print_message(msg.ERROR_NOT_IMPLEMENTED)


# print wrong option message
def print_invalid_menu_option_error():
    print_message(msg.ERROR_INVALID_OPTION)


# unhandled command
def print_unhandled_command_message(*unhandled_command):
    print("ERROR: unhandled_command: ", unhandled_command)
