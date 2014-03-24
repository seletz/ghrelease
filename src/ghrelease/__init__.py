# -*- coding: utf-8 -*-
"""ghrelease

Usage:
    ghrelease --version
    ghrelease [options] list <reponame>
    ghrelease [options] create --tag=TAG [--name=RELEASE_NAME] [--body=FILE] [--draft | --prerelease] <reponame> [<file>...]
    ghrelease [options] open (--tag=TAG | --latest) <reponame>

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
import mimetypes
import webbrowser

from .log import t
from .log import error
from .log import logger
from .log import verbose

from .cred import get_credentials

from .utils import get_repo
from .utils import print_release
from .utils import upload_assets


__version__ = "0.1"

def list_releases(gh, owner, reponame):
    """list_releases(gh, owner, reponame) -> None

    List releases command.  Loop through all releases and pretty-print
    them.

    @param gh:          the gh api handle
    @param owner:       the owner of the repo
    @param reponame:    the repository name
    """
    repo = get_repo(gh, owner, reponame)

    verbose("Listing releases of repository `%s`:" % reponame)

    for nr, release in enumerate(repo.iter_releases()):
        print_release(release)

def get_latest_release(repo):
    """get_latest_release(repo) -> release

    Fetch the latest release from the given repo and
    return it.

    @param repo:        github3 repository object
    @returns:           github3 release object or None
    """
    return repo.iter_releases(number=1).next()

def get_release(repo, tag_name):
    """get_release(repo, tag_name) -> release

    Fetch the release tagged with the given tag and
    return it.

    @param repo:        github3 repository object
    @returns:           github3 release object or None
    """
    for release in repo.iter_releases():
        if release.tag_name == tag_name:
            return release

def open_release(gh, owner, reponame, tag=None):
    """open_release(gh, owner, reponame, tag) -> None

    Open command -- find the specified release and open it's
    web page.  If the tag is not specified, the latest release
    is opened.

    @param gh:          the gh api handle
    @param owner:       the owner of the repo
    @param reponame:    the repository name
    @param tag:         the tag or None
    """

    repo = get_repo(gh, owner, reponame)

    if not tag:
        release = get_latest_release(repo)
    else:
        release = get_release(repo, tag)

    if not release:
        error(11, "No such release found.")

    webbrowser.open(release.html_url)


def create_release(gh, owner, reponame, tag, name=None, body_file=None,
                   draft=None, prerelease=None, assets=None):
    """create_release(gh, wwner, reponame, tag, ...) -> None

    Create release command.  Creates a new release for the given repository
    and tag.  The tag must exist.

    If `body_file` is specified, it is taken as a file name to read the release
    body text (release notes) from.

    @param gh:          the gh api handle
    @param owner:       the owner of the repo
    @param reponame:    the repository name
    @param tag:         the tag name
    @param name:        a name for the release (optional)
    @param body_file:   a name of a file to read the release body text from (optional)
    @param draft:       is this release a draft?  (defaults to False)
    @param prerelease:  is this release a prerelease?  (defaults to False)
    @param assets:      a list of file names (optional)
    """
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

    upload_assets(release, assets)


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
        create_release(gh, owner,
                       arguments["<reponame>"],
                       arguments["--tag"],
                       name=arguments["--name"],
                       body_file=arguments["--body"],
                       draft=arguments["--draft"],
                       prerelease=arguments["--prerelease"],
                       assets=arguments["<file>"])

    if arguments["open"]:
        open_release(gh, owner,
                     arguments["<reponame>"],
                     arguments["--tag"])

if __name__ == '__main__':
    main()

# vim: set ft=python ts=4 sw=4 expandtab :
