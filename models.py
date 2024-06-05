from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    pwd_hash = db.Column(db.String(128))

    def set_password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def validate_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)
