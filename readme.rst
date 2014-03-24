====================================
ghrelease -- a GitHub release helper
====================================

:Author:    Stefan Eletzhofer

Abstract
========

This is a little tool to help me with releasing stuff to GitHub.

Synopsis
========

::

    ghrelease - a GitHub release helper

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

Examples
========

Listing all releases of a given repository::


    $ ghrelease --user fred --pass s3kr17 list some-repo
    RELEASE    release-name (v0.3) @ https://github.com/fred/some-repo/releases/tag/v0.3
    PRERELEASE release-name (v0.2) @ https://github.com/fred/some-repo/releases/tag/v0.2
    PRERELEASE release-name (v0.1) @ https://github.com/fred/some-repo/releases/tag/v0.1

Passing credentials via command line is insecure and ugly::

    $ export GHRELEASE_USER=fred
    $ export GHRELEASE_PASS=s3kr71
    $ ghrelease list some-repo
    RELEASE    release-name (v0.3) @ https://github.com/fred/some-repo/releases/tag/v0.3
    PRERELEASE release-name (v0.2) @ https://github.com/fred/some-repo/releases/tag/v0.2
    PRERELEASE release-name (v0.1) @ https://github.com/fred/some-repo/releases/tag/v0.1

Creating a new release for tag `v0.4` named `super-duper`, using the local
file `docs/changelog.rst` as release notes, uploading some zip file::

    $ ghrelease create some-repo v0.4 --name super-duper --body docs/changelog.rst super-duper-0-4.zip
    Release created:
    RELEASE    super-duper (v0.4) @ https://github.com/fred/some-repo/releases/tag/v0.4
    uploading super-duper-0-4.zip (application/octet-stream) ...

Open the web page of that release::

    $ ghrelease open --tag v0.4 some-repo

Uploading assets to an existing release::

    $ ghrelease upload some-repo --tag v0.4 super-duper-0-4-docs.zip LICENSE
    uploading file super-duper-0-4-docs.zip (application/octet-stream) ...
    uploading file LICENSE (application/octet-stream) ...

.. vim: set ft=rst tw=75 spell nocin nosi ai sw=4 ts=4 expandtab:
