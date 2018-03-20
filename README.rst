========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-mqttcat/badge/?style=flat
    :target: https://readthedocs.org/projects/python-mqttcat
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/mqttcat.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/mqttcat

.. |commits-since| image:: https://img.shields.io/github/commits-since/martinvirtel/python-mqttcat/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/martinvirtel/python-mqttcat/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mqttcat.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/mqttcat

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mqttcat.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/mqttcat

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mqttcat.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/mqttcat


.. end-badges

Netcat for MQTT

* Free software: BSD 2-Clause License

Installation
============

::

    pip install mqttcat

Documentation
=============

https://python-mqttcat.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
