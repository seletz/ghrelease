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

    ghrelease

    Usage:
        ghrelease --version
        ghrelease [options] list <reponame>
        ghrelease [options] create --tag=TAG [--name=RELEASE_NAME] [--body=FILE] [--draft | --prerelease] <reponame>
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
file `docs/changelog.rst` as release notes::

    $ ghrelease create some-repo v0.4 --name super-duper --body docs/changelog.rst
    Release created:
    RELEASE    super-duper (v0.4) @ https://github.com/fred/some-repo/releases/tag/v0.4

Open the web page of that release::

    $ ghrelease open --tag v0.4 some-repo


.. vim: set ft=rst tw=75 spell nocin nosi ai sw=4 ts=4 expandtab:
