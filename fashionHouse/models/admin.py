from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class TimeMixin(object):
    created_at = db.Column(db.Datetime(), default=datetime.today())

class AdminModel(db.Model, TimeMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))


    def __init__(self, email, full_name, password):
        self.email = email
        self.full_name = full_name
        self.set_password(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()