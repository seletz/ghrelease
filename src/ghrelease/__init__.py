# -*- coding: utf-8 -*-
"""ghrelease

Usage:
    ghrelease --version
    ghrelease [options] list <reponame>

Options:
    -h --help           show this help
    -u --user=USER      github login name
    -p --password=PASS  github password
    --password-env=ENV  read password from system environment [default: GHRELEASE_PASS]
    --user-env=ENV      read user name from system environment [default: GHRELEASE_USER]
    --owner=OWNER       github owner [defaults to the user name]
    --debug             debug logging
    -v, --verbose       print more text
"""
from docopt import docopt

import sys
import logging
import github3

from .log import verbose
from .log import error
from .log import logger

from .cred import get_credentials


__version__ = "0.1"


def list_releases(gh, owner, reponame):
    repo = gh.repository(owner, reponame)
    if repo is None:
        error(10, "repository not found: " + reponame)

    verbose("Listing releases of repository `%s`:" % reponame)

    for nr, release in enumerate(repo.iter_releases()):
        print "%03d: %s" % (nr, release.name.encode("utf-8"))

def main():
    arguments = docopt(__doc__, version="ghrelease v%s" % __version__)

    if arguments["--debug"]:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-7s] [line %(lineno)d] %(name)s: %(message)s",
            stream=sys.stderr)
        logger.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)-7s] %(name)s: %(message)s",
            filename="ghrelease.log")
        logger.setLevel(logging.INFO)

    logger.debug("args: %r", arguments)

    username, password = get_credentials(arguments)

    if not username or not password:
        error(10, "Need username and password.")

    owner    = arguments["--owner"]
    if not owner:
        owner = username

    logger.debug("username=%s", username)
    logger.debug("owner   =%s", owner)

    gh = github3.login(username, password=password)

    if arguments["list"]:
        list_releases(gh, owner, arguments["<reponame>"])

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
