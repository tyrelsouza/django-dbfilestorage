Django-dbfilestorage
--------------------

.. image:: https://circleci.com/gh/tyrelsouza/django-dbfilestorage/tree/master.svg?style=svg
    :target: https://circleci.com/gh/tyrelsouza/django-dbfilestorage/tree/master

Custom file storage for Django that stores file data and content type in the database.
Easy to use for testing when you don't care about a filename, and just want to test file data.

Intended to be used in tests, never in production.


TODO
====

More Tests
Different django and different python versions.
Store original filename in a field, maybe?
Use original filename instead, so it honors the "upload_to" parameter.


CHANGELOG
=========

2016-12-07 [Tyrel Souza] Update Readme, move to github, gitlab wasn't functioning properly.
2016-12-07 [Tyrel Souza] Initial commits and basic project setup
