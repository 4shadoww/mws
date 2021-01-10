import logging
import importlib

from core import config_loader

# Init warning modules
waralgs = []

# Init precheck
prealgs = []

# Warning messages to print
warmsg = []

logger = logging.getLogger("infolog")


def init():
    for war in config_loader.config["war_modules"]:
        if war not in config_loader.config["ignored_war_modules"]:
            module = importlib.import_module("warscripts." + war)
            waralgs.append(module.Warning())

    for war in config_loader.config["pre_war_modules"]:
        if war not in config_loader.config["ignored_pre_war_modules"]:
            module = importlib.import_module("warscripts." + war)
            prealgs.append(module.Warning())


def check(text):
    warnings = False

    for warmeth in waralgs:
        warmeth.__init__()
        error_count = warmeth.run(text)
        if error_count > 0:
            warnings = True
            logger.critical("warning: " + warmeth.wm)

    return warnings


def precheck(text):
    warnings = False

    for warmeth in prealgs:
        warmeth.__init__()
        error_count = warmeth.run(text)
        if error_count > 0:
            warnings = True
            logger.critical("pre warning: " + warmeth.wm)

    return warnings

def append_warning(*message):
    finalmessage = ""
    for l, mes in enumerate(message):
        finalmessage += str(mes)
        if l != len(message):
            finalmessage += " "

    warmsg.append(finalmessage)

def print_warnings():
    global warmsg

    for msg in warmsg:
        logger.critical("warning: " + msg)

    warmsg = []
