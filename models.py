from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

class FeedbackUser(db.Model):

    __tablename__ = 'feedback_users'

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed_password = bcrypt.generate_password_hash(password)
        decoded_hash_password = hashed_password.decode('utf-8')

        return cls(username=username, password=decoded_hash_password, email=email, first_name = first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """authenticate a user"""

        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        return False


class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey('feedback_users.username'))

