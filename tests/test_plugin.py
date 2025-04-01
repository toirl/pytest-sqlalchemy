from _pytest.pytester import Pytester


def test_plugin(pytester: Pytester, db_url: str) -> None:
    pytester.copy_example("tests/examples/test_minimal.py")
    result = pytester.runpytest('--sqlalchemy-connect-url', db_url)
    result.assert_outcomes(passed=1)

