Changes
-------

0.2.1 (13.03.2018)
~~~~~~~~~~~~~~~~~~

* Fix behaviour under multiprocessing by recreating :class:`~sqlalchemy.engine.Engine` instance.

0.2.0 (22.02.2018)
~~~~~~~~~~~~~~~~~~
Feature release. Thanks to Sebastian Buczyński.

* Added option to create the database on each run by using ``sqlalchemy-utils``.

* Added option to run tests on multiple dynamically created databases
  (``pytest-xdist``) like ``pytest-django`` does.

0.1.1 (22.09.2017)
~~~~~~~~~~~~~~~~~~

Initial release.
