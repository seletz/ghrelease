# -*- coding: utf-8 -*-
"""ghrelease - a GitHub release helper

Usage:
    ghrelease --version
    ghrelease [options] list <reponame>
    ghrelease [options] create --tag=TAG [--name=RELEASE_NAME] [--body=FILE] [--draft | --prerelease] <reponame> [<file>...]
    ghrelease [options] upload --tag=TAG <reponame> <file>...
    ghrelease [options] open (--tag=TAG | --latest) <reponame>

The `list` command lists available releases.

The `create` command creates new releases, optionally uploading some assets.

The `upload` command uploads assets to a existing release.  It's not possible to
replace assets -- the command will complain if you're trying to upload an existing
asset.

The `open` command opens the release's web page in the system default browser.

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

from .log import t
from .log import error
from .log import logger
from .log import verbose

from .cred import get_credentials

from .commands import release_list
from .commands import release_create
from .commands import release_open
from .commands import release_upload_assets

__version__ = "0.1"


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
        release_list(gh, owner, arguments["<reponame>"])

    if arguments["create"]:
        release_create(gh, owner,
                       arguments["<reponame>"],
                       arguments["--tag"],
                       name=arguments["--name"],
                       body_file=arguments["--body"],
                       draft=arguments["--draft"],
                       prerelease=arguments["--prerelease"],
                       assets=arguments["<file>"])

    if arguments["open"]:
        release_open(gh, owner,
                     arguments["<reponame>"],
                     arguments["--tag"])

    if arguments["upload"]:
        release_upload_assets(gh, owner,
                              arguments["<reponame>"],
                              arguments["--tag"],
                              assets=arguments["<file>"])

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
