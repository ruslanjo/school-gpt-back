from typing import Any

from src.api.v1.dao.user_dao import UserDAO


class AuthService:
    def __init__(
            self,
            user_dao: UserDAO,
            jwt_config,
            token_generator,
            password_hasher
    ):
        self.user_dao = user_dao
        self.jwt_config = jwt_config.dict()
        self.token_generator = token_generator
        self.password_hasher = password_hasher

    def signup(
            self,
            login: str,
            password: str
    ):
        hashed_password = self.password_hasher.hash_password(password)
        return self.user_dao.add_user(
            login,
            hashed_password.decode('utf-8')
        )

    def login(self, login: str, password: str) -> None | dict:
        user = self.user_dao.get_user(
            login
        )
        if not user:
            return None

        check_password = self.password_hasher.compare_passwords(password, user.password)
        if not check_password:
            return None

        access_token, refresh_token = self.create_new_jwt_tokens(login=login)
        self.user_dao.add_login_history(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def create_new_jwt_tokens(self, **kwargs) -> tuple:
        access, refresh = self.token_generator.generate_refresh_and_access_tokens(
            {'login': kwargs.get('login')}
        )
        return access, refresh

    def use_refresh_token(
            self,
            refresh_token: str
    ) -> tuple[Any, Any] | None:
        result = self.token_generator.check_jwt_token(refresh_token)
        if not result.get('result'):
            return None

        request_user_login = result['data']['login']
        return self.create_new_jwt_tokens(login=request_user_login)
