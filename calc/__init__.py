import logging
from logging.handlers import RotatingFileHandler

from .controller import controller
# from .model import init_db

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
    # init_db()
    command = ["menu", "main"]
    while True:
        try:
            command = controller(command)
        except SystemExit:
            break
