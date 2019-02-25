from flask import request, url_for
from requests import Response, post
from db import db

MAILGUN_DOMAIN = "sandbox7f561dedb5d94009b5348af076ee9ae8.mailgun.org"
MAILGUN_API_KEY = "key-042f3f00253ba995bc98ed53e80b7807"
FROM_TITLE = "Stores REST API"
FROM_EMAIL = "postmaster@sandbox7f561dedb5d94009b5348af076ee9ae8.mailgun.org"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    def send_confirmation_email(self) -> Response:
        # http://localhost:5000/user_confirm/1
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        return post(
            f"http://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.email,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm your registration: {link}",
            },
        )


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
