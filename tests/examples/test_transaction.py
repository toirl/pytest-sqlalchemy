from sqlalchemy.engine import Connection


def test_transaction(transaction: Connection) -> None:
    assert isinstance(transaction, Connection)
    assert transaction.in_transaction()
