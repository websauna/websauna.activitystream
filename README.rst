.. contents:: :local:

Introduction
============

This is a Python package for websauna.activitystream, an addon for `Websauna framework <https://websauna.org>`_.

Activity stream gives you Facebook-like stream of activities and activity history for user.

Features
========

* Email push notifications

* Website built-in notification menu

* Notification history

Installation
============

Local development mode
----------------------

Activate the virtual environment of your Websauna application.

Then::

    cd activitystream  # This is the folder with setup.py file
    pip install -e .

Running the development website
===============================

Local development machine
-------------------------

Example (OSX / Homebrew)::

    psql create activitystream_dev
    ws-sync-db websauna/activitystream/conf/development.ini
    ws-pserve websauna/activitystream/conf/development.ini --reload

Running the test suite
======================

First create test database::

    # Create database used for unit testing
    psql create activitystream_test

Install test and dev dependencies (run in the folder with ``setup.py``)::

    pip install -e ".[dev,test]"

Run test suite using py.test running::

    py.test

More information
================

Please see https://websauna.org/