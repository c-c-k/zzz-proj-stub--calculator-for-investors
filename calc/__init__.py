import logging
from logging.handlers import RotatingFileHandler
from sys import argv

from .controller import controller

formater = logging.Formatter(
    "%(asctime)s %(levelname)-8s: %(name)s[%(lineno)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
file_handler = RotatingFileHandler(
        'debug.log', mode='a', maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.formatter = formater
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# logger.addHandler(file_handler)
logger.addHandler(logging.NullHandler())


def main():
    controller(["init_db", "--reset_db" in argv])
    command = None  # ["menu", "main"]
    while command is not None:
        command = controller(command)
