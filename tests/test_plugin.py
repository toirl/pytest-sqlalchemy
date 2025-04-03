import os
from pathlib import Path
from textwrap import dedent

from pytest import FixtureRequest
from _pytest.pytester import Pytester
from sqlalchemy_utils import database_exists, create_database


def test_minimal(pytester: Pytester, db_url: str) -> None:
    pytester.copy_example("tests/examples/test_minimal.py")
    result = pytester.runpytest('--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=1)


def test_transaction_fixture(pytester: Pytester, db_url: str) -> None:
    pytester.copy_example("tests/examples/test_transaction.py")
    result = pytester.runpytest('--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=1)


def test_dbsession_fixture(pytester: Pytester, db_url: str) -> None:
    pytester.copy_example("tests/examples/test_dbsession.py")
    result = pytester.runpytest('--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=1)


def test_db_schema(pytester: Pytester, new_db_url: str) -> None:
    assert not database_exists(new_db_url)
    pytester.copy_example("tests/examples/test_db_schema.py")
    result = pytester.runpytest(
        '--sqlalchemy-connect-url', new_db_url, '--sqlalchemy-manage-db'
    )
    result.assert_outcomes(passed=1)
    assert not database_exists(new_db_url)


def test_db_exists_no_keep_db(pytester: Pytester, db_url: str) -> None:
    if not database_exists(db_url):
        create_database(db_url)
    pytester.copy_example("tests/examples/test_db_schema.py")
    result = pytester.runpytest(
        '--sqlalchemy-connect-url', db_url, '--sqlalchemy-manage-db'
    )
    result.assert_outcomes(errors=1)
    assert "DB exists, remove it before proceeding" in result.stdout.str()
    assert database_exists(db_url)


def test_db_exists_keep_db(pytester: Pytester, db_url: str) -> None:
    if not database_exists(db_url):
        create_database(db_url)
    pytester.copy_example("tests/examples/test_db_schema.py")
    result = pytester.runpytest(
        '--sqlalchemy-connect-url',
        db_url,
        '--sqlalchemy-manage-db',
        '--sqlalchemy-keep-db',
    )
    result.assert_outcomes(passed=1)
    assert database_exists(db_url)


def test_connect_uri_alias(pytester: Pytester, db_url: str) -> None:
    pytester.copy_example("tests/examples/test_connect_uri.py")
    result = pytester.runpytest('--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=1)


def test_engine_with_config_file(pytester: Pytester, tmp_path: Path) -> None:
    config_path = tmp_path / "config.ini"
    config_path.write_text(
        dedent(
            """
        [DEFAULT]
        sqlalchemy.url = sqlite:///:memory:
    """
        )
    )

    pytester.copy_example("tests/examples/test_minimal.py")
    result = pytester.runpytest('--sqlalchemy-config-file', config_path)
    result.assert_outcomes(passed=1)


def test_engine_no_config_source(pytester: Pytester) -> None:
    pytester.copy_example("tests/examples/test_minimal.py")
    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    assert "Can not establish a connection to the database" in result.stdout.str()


def test_xdist_naming(pytester: Pytester, db_url: str, request: FixtureRequest) -> None:
    running_under_coverage = bool(os.environ.get("COVERAGE_RUN"))
    # Measuring coverage when running under xdist is pretty tricky:
    if running_under_coverage:
        pyproject_toml = Path(__file__).parent.parent / "pyproject.toml"
        pytester.makeconftest(dedent(f"""
            import coverage, os, sys
            def pytest_configure(config):
                worker_id = os.environ.get("PYTEST_XDIST_WORKER")
                if worker_id is not None:
                    os.environ["COVERAGE_PROCESS_START"] = "{pyproject_toml}"
                    coverage.process_startup()
        """))
    pytester.copy_example("tests/examples/test_xdist.py")
    result = pytester.runpytest('-n', '2', '--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=2)
    if running_under_coverage:
        for item in pytester.path.glob('.coverage.*'):
            item.rename(request.config.rootdir / item.name)
