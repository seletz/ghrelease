# -*- coding: utf-8 -*-

import mimetypes

from .log import t
from .log import error
from .log import logger
from .log import verbose

def guess_mimetype(filename, default='application/octet-stream'):
    tp, encoding = mimetypes.guess_type(filename)
    return tp or default


def get_repo(gh, owner, reponame):
    """get_repo(gh, owner, reponame) -> repo

    Get a repo and error out if no repo found.

    @param gh:          the gh api handle
    @param owner:       the owner of the repo
    @param reponame:    the repository name
    @returns:           repository object
    """
    repo = gh.repository(owner, reponame)
    if repo is None:
        error(10, "repository not found: " + reponame)

    return repo

def print_release(release):
    """print_release(release) -> None

    Simple helper to pretty-print a release.

    @param release:     a github3 release object
    """
    name = release.name or "<no name>"
    m = u"%s (%s) @ %s" % (name, release.tag_name, release.html_url)
    if release.prerelease:
        print t.yellow("PRERELEASE"),
    elif release.draft:
        print t.blue("DRAFT     "),
    else:
        print t.green("RELEASE   "),

    print m.encode("utf-8")

def get_assets(release):
    return {asset.name: asset for asset in release.iter_assets()}

def upload_assets(release, assets):

    existing_assets = get_assets(release)

    for filename in assets:
        existing = existing_assets.get(filename)
        if existing:
            error(12, "Asset `%s` already exists: `%s/%s`" % (filename, release.html_url, existing.name))

        logger.debug("processing: %s", filename)
        mime_type = guess_mimetype(filename)
        logger.debug("mime type: %s", mime_type)

        with file(filename, "rb") as f:
            verbose("uploading file %s (%s) ..." % (filename, mime_type))
            logger.debug("uploading ....")
            release.upload_asset(mime_type, filename, f)

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

# vim: set ft=python ts=4 sw=4 expandtab :
