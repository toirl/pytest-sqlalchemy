from sqlalchemy.orm import Session


def test_session(dbsession):
    assert isinstance(dbsession, Session)
