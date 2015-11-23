# pytest-sqlalchemy
SQLAlchemy related fixtures to handle connections and transactions with SQLAlchemy in tests.

## Fixtures
This plugin provides the following fixtures:

1. **engine** The engine used to connect to the database. Scope is "module".
1. **connection** An open connection to the database. Scope is "module".
1. **transaction** A started transaction on the connection. Transaction will be rolled back. No Scope.
1. **dbsession** A sqlalchemy session *not* bound to any model. No scope.

## Invoke
You need to provide the connection URL for the engine when invoking the pytest command::

    py-test --sqlalchemy-connect-url="postgresql://scott:tiger@localhost:5432/mydatabase"
