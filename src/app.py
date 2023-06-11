from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_migrate import Migrate

from src.db import init_db, db
from src.container import app_config
from src.api.v1.views.gpt import gpt_ns
from src.api.v1.views.auth import auth_ns


api = Api(title='School-GPT', docs='/docs')
migrate = Migrate()


def create_app(rest_api: Api, config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    register_extensions(application, rest_api)
    return application


def register_extensions(application: Flask, rest_api: Api) -> None:
    init_db(application)
    rest_api.init_app(application)
    migrate.init_app(application, db)
    rest_api.add_namespace(gpt_ns)
    rest_api.add_namespace(auth_ns)
    CORS(application)


app = create_app(api, app_config)


if __name__ == '__main__':
    app.run('0.0.0.0', port=6001)
