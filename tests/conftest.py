import os

import pytest

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session")
def db_url() -> str:
    return os.environ.get("DB_URL", "sqlite:///:memory:")
