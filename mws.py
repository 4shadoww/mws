#!/usr/bin/env python3

import sys
import os
import logging
import argparse

from core import config_loader
from core import path
from core import session
from core import task_handler

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,)

class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        return 1 if record.levelno < self.max_level else 0

def setup_argparser():
    parser.add_argument("--pages", "-p", help="pages to be checked", required=False, nargs='+')
    parser.add_argument("--pages-file", "-pf", help="load pages to be checked from file", required=False)
    parser.add_argument("--config-file", "-cf", help="set configuration file path", required=False)
    parser.add_argument("--scripts", "-s", help="scripts to be runned (overwrites configuration file's list)", required=False, nargs='+')
    parser.add_argument("--test-file", "-tf", help="load test article from file", required=False, nargs='+')
    parser.add_argument("--ignored-scripts", "-is", help="scripts to be ignored", required=False, nargs='+')
    parser.add_argument("--review", "-r", help="show diff before saving", required=False, action="store_true")
    parser.add_argument("--test", "-t", help="don't save changes", required=False, action="store_true")
    parser.add_argument("--tests", "-ts", help="tests to be run", required=False, nargs='+')
    parser.add_argument("--ignored-tests", "-its", help="ignored tests", required=False, nargs='+')

def setup_logging():
    # Logging
    logger = logging.getLogger("infolog")
    logger.setLevel(logging.DEBUG)
    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # Stream
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.addFilter(LessThanFilter(logging.ERROR))
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    # Error stream
    eh = logging.StreamHandler(sys.stderr)
    eh.setLevel(logging.ERROR)
    eh.setFormatter(formatter)
    logger.addHandler(eh)
    # Info log
    if config_loader.config["enable_log"]:
        il = logging.FileHandler(path.main()+"logs/info.log")
        il.setLevel(logging.DEBUG)
        il.addFilter(LessThanFilter(logging.ERROR))
        il.setFormatter(formatter)
        logger.addHandler(il)
    # Error log
    el = logging.FileHandler(path.main()+"logs/crashreport.log")
    el.setLevel(logging.ERROR)
    el.setFormatter(formatter)
    logger.addHandler(el)

def run_given_task(args):
    pages = args.pages
    # Read pages from file
    if args.pages_file:
        pages = []
        with open(args.pages_file, "r") as pages_file:
            for line in pages_file:
                if(not line.isspace()): pages.append(line.rstrip())

    elif args.test_file:
        pages = [""]

    if len(config_loader.config["tests"]) > 0:
        task_handler.run(pages, run_tests=True)
    else:
        task_handler.run(pages, run_tests=False)

def main():
    try:
        # Parse args
        setup_argparser()
        args = parser.parse_args()

        # Load config
        if (args.config_file and not config_loader.load_config(filename=args.config_file)) or (not args.config_file and not config_loader.load_config()):
            print("Created new default config")

        if "help" in args:
            parser.print_help()
            sys.exit(0)

        # Save args to config
        # Save review
        if args.review:
            config_loader.config["review"] = args.review

        # Save test
        if args.test:
            config_loader.config["test"] = args.test

        # Save tests and ignore tests
        if args.tests:
            config_loader.config["tests"] = args.tests
        if args.ignored_tests:
            config_loader.config["ignored_tests"] = args.ignored_tests

        if not args.pages and not args.pages_file and not args.test_file:
            sys.stderr.write("error: no pages or pages file\n")
            parser.print_help()
            sys.exit(1)
        elif args.pages and args.pages_file:
            sys.stderr.write("error: no --pages and --pages-file can be defined at the same time\n")
            parser.print_help()
            sys.exit(1)

        # Save scripts
        if args.scripts:
            config_loader.config["scripts"] = args.scripts
        elif not args.tests:
            print("no scripts given")
            parser.print_help()
            sys.exit(1)
        # Save ignored scripts
        if args.ignored_scripts:
            config_loader.config["ignored_scripts"] = args.ignored_scripts
        elif not args.tests and not args.scripts:
            print("no scripts given")
            parser.print_help()
            sys.exit(1)
        # Save test file
        if args.test_file:
            config_loader.config["test_file"] = args.test_file[0]
        # Create logging directory
        try:
            os.makedirs(config_loader.config["log_directory"])
        except FileExistsError:
            pass
        # Set up logger
        setup_logging()
        # Get logger
        logger = logging.getLogger("infolog")

        # Login
        session.create()
        session.login()

        run_given_task(args)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt on main(): closing...")

if(__name__ == "__main__"):
    main()
