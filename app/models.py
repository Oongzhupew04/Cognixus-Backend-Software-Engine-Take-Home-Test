from app import db
from sqlalchemy import ForeignKey

class UserAccounts(db.Model):
    __tablename__ = 'UserAccounts'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, email, password):
        self.email = email
        self.password = password


class TodoList(db.Model):
    __tablename__ = 'TodoList'

    todo_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, ForeignKey('UserAccounts.user_id'))

    def __repr__(self):
        return self.text
