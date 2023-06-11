import datetime

from src.models import User, Visit


class UserDAO:
    def __init__(self, session):
        self.session = session

    def add_user(self, login: str, password: str) -> User:
        new_user = User(
            login=login,
            password=password
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user(self, login: str) -> [None | tuple[str, str]]:
        return self.session.query(User).filter(User.login == login).first()

    def update(self, updated_entity: User):
        self.session.add(updated_entity)
        self.session.commit()
        return updated_entity

    def add_login_history(self, user_id: int) -> Visit:
        visit = Visit(
            timestamp=datetime.datetime.utcnow(),
            user_id=user_id,
        )
        self.session.add(visit)
        self.session.commit()
        return visit
