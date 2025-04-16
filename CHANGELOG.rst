Changes
-------

0.3.0 (16.04.2025)
~~~~~~~~~~~~~~~~~~

* Now targeting Python 3.9+, SQLAlchemy 1.4+ and pytest 8+.

* Moved to `uv`__ for environment management and `Github Actions`__ for CI.

* Testing against sqlite, MySQL and Postgres, with 100% line coverage.

* Fully type annotated and checked with `mypy`__.

* Formatted with `ruff`__.

* Documentation moved to `Sphinx`__ and published on `Read the Docs`__

__ https://docs.astral.sh/uv/

__ https://github.com/pytest-dev/pytest-sqlalchemy/actions

__ https://mypy.readthedocs.io/en/stable/

__ https://docs.astral.sh/ruff/

__ https://www.sphinx-doc.org/en/master/

__ https://pytest-sqlalchemy.readthedocs.io/

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
