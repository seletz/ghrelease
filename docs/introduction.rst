============
Introduction
============

:Author:    Stefan Eletzhofer
:Date:      |today|

Problem Statement
=================

When developing software we need to release the software to some known location
where our users are able to download the software.

I very much like to use `git` to tag releases, and I like the way GitHub
has integrated releases.

However, I don't like to manually upload stuff using web browsers --
however convenient drag and drop may be -- I very much like to automate the
release process.

Unfortunately, it seems that there's no command line tool for that.  This
project aims to add such a tool.

Goals
=====

I want to have a **command line tool** which allows me to:

- **create** releases for projects hosted on GitHub, specifying release
  notes and asset files

- **list** releases

- **alter** the state of releases, e.g. from `draft` to `prerelese` to
  `release`


Non-Goals
=========

- Only GitHub

- No framework for automating things -- just a CLI tool which does create
  releases.


Repository, Issue Tracker
=========================

**repository**
    git@github.com:seletz/ghrelease.git

**issue tracker**
    https://github.com/seletz/ghrelease/issues

.. vim: set spell spelllang=en ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:


