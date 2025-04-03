import os
from pathlib import Path

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture()
def db_url(tmp_path: Path) -> str:
    return os.environ.get("DB_URL", "sqlite:///" + str(tmp_path / "test.db"))


@pytest.fixture()
def new_db_url(db_url: str) -> str:
    """A db_url pointing at a database that does not exist"""
    return db_url + '_new'
