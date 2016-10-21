Go Contacts Exporter
=============================

.. image:: https://img.shields.io/travis/smn/go-contacts-exporter.svg
        :target: https://travis-ci.org/smn/go-contacts-exporter

.. image:: https://img.shields.io/pypi/v/Go Contacts Exporter.svg
        :target: https://pypi.python.org/pypi/Go Contacts Exporter

.. image:: https://coveralls.io/repos/smn/go-contacts-exporter/badge.png?branch=develop
    :target: https://coveralls.io/r/smn/go-contacts-exporter?branch=develop
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/Go Contacts Exporter/badge/?version=latest
    :target: https://Go Contacts Exporter.readthedocs.org
    :alt: Go Contacts Exporter Docs


To create a db::

    python -m go_contacts_exporter.init_db --engine="postgresql://localhost/contacts"

To export contacts to the db::

    python -m go_contacts_exporter.export --token=<your token here> --engine="postgresql://localhost/contacts"
