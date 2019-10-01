from datetime import datetime

from passlib.hash import pbkdf2_sha256 as sha256

from flaskapi import db


class BaseModel(object):
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_active = False
        db.session.commit()


class User(db.Model, BaseModel):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(100),
        nullable=False
    )
    password = db.Column(
        db.String(100),
        nullable=False
    )
    doc_number = db.Column(
        db.String(100),
        nullable=False
    )
    balance = db.Column(
        db.Float,
        default=0.0
    )
    is_active = db.Column(
        db.Boolean,
        default=True
    )

    __to_dict_fields__ = {
        'id': id,
        'email': email,
        'doc_number': doc_number,
        'balance': balance
    }

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            doc_number=self.doc_number,
            balance=self.balance
        )

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_doc_number(cls, doc_number):
        return cls.query.filter_by(doc_number=doc_number).first()
