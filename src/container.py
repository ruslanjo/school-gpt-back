from src.config import AppConfig, AuthConfig
from src.core.auth.tokens_generator import TokenGenerator, PasswordHasher
from src.db import db
from src.api.v1.dao.user_dao import UserDAO
from src.api.v1.services.auth import AuthService

############################ CONFIGS ############################
app_config = AppConfig()
auth_config = AuthConfig()

############################ UTILS ############################
token_generator = TokenGenerator(auth_config)
password_hasher = PasswordHasher()

############################ DAO ############################
user_dao = UserDAO(db.session)

############################ SERVICES ############################
auth_service = AuthService(user_dao, auth_config, token_generator, password_hasher)
