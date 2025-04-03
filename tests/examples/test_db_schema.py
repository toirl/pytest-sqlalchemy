from sqlalchemy.engine import Engine
from sqlalchemy_utils import database_exists


def test_db_schema(db_schema: None, engine: Engine) -> None:
    assert db_schema is None  # Not very helpful?
    assert database_exists(engine.url)
