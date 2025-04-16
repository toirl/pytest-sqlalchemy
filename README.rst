pytest-sqlalchemy
=================

|Docs|_  |PyPI|_ |Git|_

.. |Docs| image:: https://readthedocs.org/projects/pytest-sqlalchemy/badge/?version=latest
.. _Docs: https://pytest-sqlalchemy.readthedocs.io/

.. |PyPI| image:: https://badge.fury.io/py/pytest-sqlalchemy.svg
.. _PyPI: https://pypi.org/project/pytest-sqlalchemy/

.. |Git| image:: https://github.com/toirl/pytest-sqlalchemy/actions/workflows/ci.yml/badge.svg
.. _Git: https://github.com/toirl/pytest-sqlalchemy

SQLAlchemy related fixtures to handle connections and transactions with SQLAlchemy in tests.

Fixtures
--------
This plugin provides the following fixtures which gives access to the SQLAlchemy objects of the same 
name.

* **engine** The engine used to connect to the database. Scope is "module".
* **connection** An open connection to the database. Scope is "module".

See `Working with Engines and Connections`__ on how to use these fixtures.

__ http://docs.sqlalchemy.org/en/latest/core/connections.html#module-sqlalchemy.engine

* **transaction** A started transaction on the connection. Transaction will be rolled back.
  No Scope.

See `Using Transactions`__ on how to use this fixtures

__ http://docs.sqlalchemy.org/en/latest/core/connections.html#using-transactions

* **dbsession** A sqlalchemy session *not* bound to any model. No scope.

See `Session Basics`__ to learn about how to use sessions.

__ http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-basics

Usage
-----
The fixtures can be used in your tests like any other `Pytest Fixtures`__.

__ https://docs.pytest.org/en/3.6.1/fixture.html

**Example**:

.. code-block:: python

    import pytest
    from pytest_sqlalchemy import connection
    
    def test_connection(connection):
        # Do fancy stuff with the connection.
        # Note you will not need to close the connection. This is done
        # automatically when the scope (module) of the fixtures ends.
        assert connection

Invoke
------
You need to provide the connection URL for the engine when invoking the pytest command:

.. code-block:: bash

    pytest --sqlalchemy-connect-url="postgresql://scott:tiger@localhost:5432/mydatabase"
    
Or override the ``sqlalchemy_connect_url`` fixture on your ``conftest.py`` file:

.. code-block:: python

    @pytest.fixture(scope="session")
    def sqlalchemy_connect_url():
        return 'postgresql://scott:tiger@localhost:5432/mydatabase'

Development
-----------

To get going, in a checkout:

.. code-block:: bash

    uv sync

You can then run the tests with:

.. code-block:: bash

    uv run pytest
