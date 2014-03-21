# -*- coding: utf-8 -*-

import sys
import colorama
import blessings
import logging

logger = logging.getLogger("ghrelease")

t = blessings.Terminal()

debug = logger.debug
info  = logger.info


def error(code, message):
    logger.error(message)
    print t.red("[ERROR] " + message)
    sys.exit(code)

def verbose(message):
    logger.info(message)
    print t.green(message)

# vim: set ft=python ts=4 sw=4 expandtab :
