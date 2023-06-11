import os
from enum import Enum

from pydantic import BaseSettings, Field


basedir = os.path.abspath(os.path.dirname(__file__))


class ModelEnvironments(Enum):
    dev = 'DEV'
    prod = 'PROD'


class AuthConfig(BaseSettings):
    access_token_lifetime: int = Field(default=60000, env='JWT_ACCESS_LIFETIME')
    refresh_token_lifetime: int = Field(default=86400, env='JWT_REFRESH_LIFETIME')


class AppConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_ENVIRONMENT = ModelEnvironments.dev


print(AppConfig().SQLALCHEMY_DATABASE_URI)