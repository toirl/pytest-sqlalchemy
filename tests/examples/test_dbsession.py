from sqlalchemy.orm import Session


def test_session(dbsession: Session) -> None:
    assert isinstance(dbsession, Session)
