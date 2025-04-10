from sqlalchemy.engine import Engine


def test_one(engine: Engine) -> None:
    db_name = str(engine.url.database) if engine.url.database is not None else ""
    assert '_gw' in db_name


def test_two(engine: Engine) -> None:
    db_name = str(engine.url.database) if engine.url.database is not None else ""
    assert '_gw' in db_name
