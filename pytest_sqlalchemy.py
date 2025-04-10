#!/usr/bin/env python
# encoding: utf-8

from typing import Any, Dict, Mapping, Optional

import pytest
import sqlalchemy_utils.functions
from pytest import FixtureRequest, Parser
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Connection, create_engine, Engine


@pytest.fixture(scope="session")
def engine(
    request: FixtureRequest,
    sqlalchemy_connect_url: Optional[str],
    app_config: Optional[Dict[str, str]],
) -> Engine:
    """Engine configuration.
    See http://docs.sqlalchemy.org/en/latest/core/engines.html
    for more details.

    :sqlalchemy_connect_url: Connection URL to the database. E.g
    postgresql://scott:tiger@localhost:5432/mydatabase
    :app_config: Path to a ini config file containing the sqlalchemy.url
    config variable in the DEFAULT section.
    :returns: Engine instance

    """
    if app_config:
        engine = engine_from_config(app_config)
    elif sqlalchemy_connect_url:
        engine = create_engine(sqlalchemy_connect_url)
    else:
        raise RuntimeError("Can not establish a connection to the database")

    # Put a suffix like _gw0, _gw1 etc on xdist processes
    xdist_suffix = getattr(request.config, 'workerinput', {}).get('workerid')
    print(xdist_suffix)
    if engine.url.database != ':memory:' and xdist_suffix is not None:
        url = engine.url.set(database=f'{engine.url.database}_{xdist_suffix}')
        engine = create_engine(url)  # override engine

    def fin() -> None:
        print("Disposing engine")
        engine.dispose()

    request.addfinalizer(fin)
    return engine


@pytest.fixture(scope="session")
def db_schema(
    request: FixtureRequest, engine: Engine, sqlalchemy_manage_db: bool, sqlalchemy_keep_db: bool
) -> None:
    if not sqlalchemy_manage_db:
        return

    db_exists = sqlalchemy_utils.functions.database_exists(engine.url)
    if db_exists and not sqlalchemy_keep_db:
        raise RuntimeError("DB exists, remove it before proceeding")

    if not db_exists:
        sqlalchemy_utils.functions.create_database(engine.url)

    if not sqlalchemy_keep_db:

        def fin() -> None:
            print("Tearing down DB")
            sqlalchemy_utils.functions.drop_database(engine.url)

        request.addfinalizer(fin)


@pytest.fixture(scope="module")
def connection(request: FixtureRequest, engine: Engine, db_schema: Optional[None]) -> Connection:
    connection = engine.connect()

    def fin() -> None:
        print("Closing connection")
        connection.close()

    request.addfinalizer(fin)
    return connection


@pytest.fixture()
def transaction(request: FixtureRequest, connection: Connection) -> Connection:
    """Will start a transaction on the connection. The connection will
    be rolled back after it leaves its scope."""
    transaction = connection.begin()

    def fin() -> None:
        print("Rollback")
        transaction.rollback()

    request.addfinalizer(fin)
    return connection


@pytest.fixture()
def dbsession(request: FixtureRequest, connection: Connection) -> Any:
    from sqlalchemy.orm import sessionmaker

    return sessionmaker()(bind=connection)


# Config options
@pytest.fixture(scope="session")
def sqlalchemy_connect_url(request: FixtureRequest) -> Optional[str]:
    return request.config.getoption("--sqlalchemy-connect-url")


@pytest.fixture(scope="session")
def connect_uri(request: FixtureRequest, sqlalchemy_connect_url: Optional[str]) -> Optional[str]:
    return sqlalchemy_connect_url


@pytest.fixture(scope="session")
def sqlalchemy_manage_db(request: FixtureRequest) -> Optional[bool]:
    return request.config.getoption("--sqlalchemy-manage-db")


@pytest.fixture(scope="session")
def sqlalchemy_keep_db(request: FixtureRequest) -> Optional[bool]:
    return request.config.getoption("--sqlalchemy-keep-db")


@pytest.fixture(scope="session")
def app_config(request: FixtureRequest) -> Optional[Mapping[str, str]]:
    """Example of a config file:

    [DEFAULT]
    sqlalchemy.url = postgresql://scott:tiger@localhost/test
    """
    import configparser as ConfigParser

    config_path = request.config.getoption("--sqlalchemy-config-file")
    if config_path:
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config.defaults()
    return None


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--sqlalchemy-connect-url",
        action="store",
        default=None,
        help="Name of the database to connect to",
    )

    parser.addoption(
        "--sqlalchemy-config-file",
        action="store",
        default=None,
        help="Path to a config file containing the "
        "'sqlalchemy.url' variable in the DEFAULT section "
        "of a ini file to define the connect "
        "url.",
    )

    parser.addoption(
        "--sqlalchemy-manage-db",
        action="store_true",
        default=None,
        help="Automatically creates and drops database",
    )

    parser.addoption(
        "--sqlalchemy-keep-db",
        action="store_true",
        default=None,
        help="Do not delete database after test suite, allowing for its reuse.",
    )
