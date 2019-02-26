from typing import List
from requests import Response, post


class Mailgun:
    MAILGUN_DOMAIN = "sandbox7f561dedb5d94009b5348af076ee9ae8.mailgun.org"
    MAILGUN_API_KEY = "key-042f3f00253ba995bc98ed53e80b7807"

    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "postmaster@sandbox7f561dedb5d94009b5348af076ee9ae8.mailgun.org"

    @classmethod
    def send_email(cls, email: List(str), subject: str, text: str, html: str) -> Response:
        # http://localhost:5000/user_confirm/1
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)
        return post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html
            },
        )