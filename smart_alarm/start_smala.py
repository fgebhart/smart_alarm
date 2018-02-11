#!/usr/bin/env python

import argparse
import logging
import config


def build_logger(logging_level):
    # set up logging
    logging.basicConfig(filename=config.logfile,
                        level=logging_level,
                        format='%(asctime)s :: '
                               '%(levelname)s :: '
                               '%(funcName)s in %(pathname)s :: '
                               '%(message)s')


def enable_console_logging(logging_level):
    # enable logging in console with stream handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    formatter = logging.Formatter('%(levelname)s :: '
                                  '%(funcName)s in %(pathname)s (l:%(lineno)d) :: '
                                  '%(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger("").addHandler(console_handler)


def build_parser():
    # create parser to handle arguments
    parser = argparse.ArgumentParser(prog="Start script for Smala",
                                     description="Use this script for developing and debugging Smala")
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument("--start", help="start smala, action="store_true")
    # group.add_argument("--stop", help="stop smala, action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug logging mode", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    # parser.add_argument("-a", "--argument", type=str, help="provide optional argument")
    args = parser.parse_args()
    return args, parser


def manager():
    args, parser = build_parser()
    # default logging level
    log_lvl = logging.INFO
    if args.debug:
        log_lvl = logging.DEBUG

    # initialize logging module
    build_logger(log_lvl)

    if args.verbose:
        enable_console_logging(log_lvl)

    logging.debug("Logger started in {}-mode".format(logging.getLevelName(log_lvl)))

    import smart_alarm


if __name__ == '__main__':
    # start manager
    manager()
