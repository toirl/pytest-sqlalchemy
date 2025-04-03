from sqlalchemy.engine import Connection


def test_transaction(transaction):
    assert isinstance(transaction, Connection)
    assert transaction.in_transaction()
