# -*- coding: utf-8 -*-
"""ghrelease

Usage:
    ghrelease --version
    ghrelease [options] list <reponame>
    ghrelease [options] create --tag=TAG [--name=RELEASE_NAME] [--body=FILE] [--draft | --prerelease] <reponame>

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


__version__ = "0.1"

def get_repo(gh, owner, reponame):
    repo = gh.repository(owner, reponame)
    if repo is None:
        error(10, "repository not found: " + reponame)

    return repo

def print_release(release):
    name = release.name or "<no name>"
    m = u"%s (%s) @ %s" % (name, release.tag_name, release.html_url)
    if release.prerelease:
        print t.yellow("PRERELEASE"),
    elif release.draft:
        print   t.blue("DRAFT     "),
    else:
        print  t.green("RELEASE   "),

    print m.encode("utf-8")

def list_releases(gh, owner, reponame):
    repo = get_repo(gh, owner, reponame)

    verbose("Listing releases of repository `%s`:" % reponame)

    for nr, release in enumerate(repo.iter_releases()):
        print_release(release)

def create_release(gh, owner, reponame, tag, name=None, body_file=None, draft=None, prerelease=None):
    repo = get_repo(gh, owner, reponame)

    body = None
    if body_file:
        with file(body_file, "r") as f:
            body = f.read()

    release = repo.create_release(
        tag,
        name=name,
        body=body,
        draft=draft,
        prerelease=prerelease)

    verbose("Release created:")
    print_release(release)

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

    if arguments["create"]:
        create_release(gh, owner, arguments["<reponame>"],
            arguments["--tag"],
            name=arguments["--name"],
            body_file=arguments["--body"],
            draft=arguments["--draft"],
            prerelease=arguments["--prerelease"])

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
