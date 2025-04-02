from sqlalchemy.engine import Connection


def test_connection(connection):
    assert isinstance(connection, Connection)
    assert not connection.in_transaction()
