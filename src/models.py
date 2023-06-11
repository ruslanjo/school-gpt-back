from sqlalchemy.orm import relationship

from src.db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, nullable=False)
    question = db.Column(db.Text, nullable=False)
    model_answer = db.Column(db.Text, nullable=False)
    is_pending = db.Column(db.Boolean, nullable=False)
    user = relationship('User', backref='conversations')


class Visit(db.Model):
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.ForeignKey('users.id'))
    user = relationship('User', backref='visits')
