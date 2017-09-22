#!/usr/bin/env python
# encoding: utf-8

import pytest


@pytest.fixture(scope="session")
def engine(request, sqlalchemy_connect_url, app_config):
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
        from sqlalchemy import engine_from_config
        engine = engine_from_config(app_config)
    elif sqlalchemy_connect_url:
        from sqlalchemy.engine import create_engine
        engine = create_engine(sqlalchemy_connect_url)
    else:
        raise RuntimeError("Can not establish a connection to the database")

    def fin():
        print ("Disposing engine")
        engine.dispose()

    request.addfinalizer(fin)
    return engine


@pytest.fixture(scope="module")
def connection(request, engine):
    connection = engine.connect()

    def fin():
        print ("Closing connection")
        connection.close()

    request.addfinalizer(fin)
    return connection


@pytest.fixture()
def transaction(request, connection):
    """Will start a transaction on the connection. The connection will
    be rolled back after it leaves its scope."""
    transaction = connection.begin()

    def fin():
        print ("Rollback")
        transaction.rollback()

    request.addfinalizer(fin)
    return connection


@pytest.fixture()
def dbsession(request, connection):
    from sqlalchemy.orm import sessionmaker
    return sessionmaker()(bind=connection)


# Config options
@pytest.fixture(scope="session")
def sqlalchemy_connect_url(request):
    return request.config.getoption("--sqlalchemy-connect-url")


@pytest.fixture(scope="session")
def app_config(request):
    """Example of a config file:

    [DEFAULT]
    sqlalchemy.url = postgresql://scott:tiger@localhost/test
    """
    try:
        import ConfigParser
    except ImportError:
        import configparser as ConfigParser

    config_path = request.config.getoption("--sqlalchemy-config-file")
    if config_path:
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config.defaults()
    return None


def pytest_addoption(parser):
    parser.addoption("--sqlalchemy-connect-url", action="store",
                     default=None,
                     help="Name of the database to connect to")

    parser.addoption("--sqlalchemy-config-file", action="store",
                     default=None,
                     help="Path to a config file containing the "
                     "'sqlalchemy.url' variable in the DEFAULT section "
                     "of a ini file to define the connect "
                     "url.")
