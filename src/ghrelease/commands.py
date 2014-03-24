# -*- coding: utf-8 -*-

import mimetypes
import webbrowser

from .log import t
from .log import error
from .log import logger
from .log import verbose

from .utils import get_repo
from .utils import get_latest_release
from .utils import get_release
from .utils import print_release
from .utils import get_assets
from .utils import upload_assets

def release_list(gh, owner, reponame):
    """release_list(gh, owner, reponame) -> None

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

def release_open(gh, owner, reponame, tag=None):
    """release_open(gh, owner, reponame, tag) -> None

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

def release_create(gh, owner, reponame, tag, name=None, body_file=None,
                   draft=None, prerelease=None, assets=None):
    """release_create(gh, wwner, reponame, tag, ...) -> None

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

def release_upload_assets(gh, owner, reponame, tag, assets):
    """release_upload_assets(gh, owner, reponame, tag, assets) -> None

    Upload assets to an existing release.

    @param gh:          the gh api handle
    @param owner:       the owner of the repo
    @param reponame:    the repository name
    @param tag:         the tag name
    @param assets:      a list of file names
    """
    logger.debug("release_upload_assets: reponame=%s, tag=%s, assets=%r", reponame, tag, assets)
    repo = get_repo(gh, owner, reponame)

    release = get_release(repo, tag)
    if not release:
        error(10, "No release found for tag '%s'." % tag)

    upload_assets(release, assets)


# vim: set ft=python ts=4 sw=4 expandtab :
