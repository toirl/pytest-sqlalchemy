# pytest-sqlalchemy
SQLAlchemy related fixtures to handle connections and transactions with SQLAlchemy in tests.

**This package isn't actively maintained anymore.** I wrote it years ago to make testing more easy in my own project. I was (and still am) happy that it is useful to some other people. However I don't find time to work on this project anymore. If you are interested in taking over the maintainance, please reach out to me.

## Fixtures
This plugin provides the following fixtures which gives access to the SQLAlchmey objects of the same name.

* **engine** The engine used to connect to the database. Scope is "module".
* **connection** An open connection to the database. Scope is "module".

See [Working with Engines and Conncetions](http://docs.sqlalchemy.org/en/latest/core/connections.html#module-sqlalchemy.engine) on how to use this fixtues.

* **transaction** A started transaction on the connection. Transaction will be rolled back. No Scope.

See [Using Transactions](http://docs.sqlalchemy.org/en/latest/core/connections.html#using-transactions) on how to use this fixtures

* **dbsession** A sqlalchemy session *not* bound to any model. No scope.

See [Session Basisc](http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-basics) to learn about how to use sessions.

## Usage
The fixtures can be used in your tests like any other [Pytest Fixtures](https://docs.pytest.org/en/3.6.1/fixture.html).

**Example**:

```python
import pytest
from pytest_sqlalchemy import connection

def test_connection(connection):
    # Do fancy stuff with the connection.
    # Note you will not need to close the connection. This is done
    # automatically when the scope (module) of the fixtures ends.
    assert connection
````

## Invoke
You need to provide the connection URL for the engine when invoking the pytest command::

    pytest --sqlalchemy-connect-url="postgresql://scott:tiger@localhost:5432/mydatabase"
    
Or override the `sqlalchemy_connect_url` fixture on your conftest file:

    @pytest.fixture(scope="session")
    def sqlalchemy_connect_url():
        return 'postgresql://scott:tiger@localhost:5432/mydatabase'

## Development

To get going, in a checkout:

```bash
uv sync
```

You can then run the tests with:

```bash
uv run pytest
```
