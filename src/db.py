from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(application: Flask):
    db.init_app(application)
    from src.models import (
        User, Conversation, Visit
    )
