import json
import os

from core import path

algorithms = ["brfix",
               "centerfix", "smallfix", "titlechanger",
               "textinen", "seealsotoexl", "twovlines", "reftosrc", "titlelevel",
               "refstemp", "fix2brackets",  "fixpiped", "fixreflist", "replacecomms", "replacesrc", "replaceseealso", "replaceli",]

config = {
    "lang": "en",
    "enable_log": True,
    "review": False,
    "test": False,
    "minor": True,
    "allow_zero": False,
    "log_directory": "logs",
    "site": "http://127.0.0.1",
    "api_path": "/api.php",
    "scripts": algorithms,
    "ignored_scripts": [],
    "tests": [],
    "ignored_tests": [],
    "pre_war_modules": ["notvalidsec"],
    "ignored_pre_war_modules": [],
    "war_modules": ["refsec", "secorder", "srcsrefsec", "danreftemp", "titlewithoutcontent", "level3srcs", "catnotbelow", "toomanyrefs", "comments"],
    "ignored_war_modules": [],
    "throttle": 5
}

def merge_config(to_config, from_config):
    for key in from_config:
        to_config[key] = from_config[key]

    return to_config

def load_config(filename=path.main() + "mws.json"):
    global config

    # TODO allow to set the config file from command line
    if not os.path.isfile(filename):
        with open(filename, "w") as config_f:
            json.dump(config, config_f, indent=2, separators=(',', ': '))

        return False

    with open(filename, "r") as config_f:
        temp_config = json.load(config_f)

    merge_config(config, temp_config)

    return True
