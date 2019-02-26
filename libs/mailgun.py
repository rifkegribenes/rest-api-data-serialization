import os
from typing import List
from requests import Response, post

API_KEY_LOAD_FAILURE = "Failed to load Mailgun API key."
MG_DOMAIN_LOAD_FAILURE = "Failed to load Mailgun domain."
ERROR_SENDING_EMAIL = "Error sending confirmation email. User registration failed."


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "postmaster@sandbox7f561dedb5d94009b5348af076ee9ae8.mailgun.org"

    @classmethod
    def send_email(cls, email: List(str), subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(API_KEY_LOAD_FAILURE)

        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(MG_DOMAIN_LOAD_FAILURE)

        response = post(
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

        if response.status_code != 200:
            raise MailgunException(ERROR_SENDING_EMAIL)

        return response