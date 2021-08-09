import logging
import requests

import jinja2
from typing import Any, Dict

from config import settings


class MailingService:
    __instance = None

    @staticmethod
    def get_instance():
        if MailingService.__instance is None:
            MailingService()

        return MailingService.__instance

    def __init__(self):
        if MailingService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MailingService.__instance = self

    def send(
        self,
        template: str,
        to: str,
        variables: Dict[str, Any] = {},
        subject: str = "Hello from Whispers!",
    ):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template)
        rendered_template = template.render(**variables)

        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_KEY),
            data={
                "from": f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_ADDRESS}>",
                "to": to,
                "subject": subject,
                "html": rendered_template,
            },
        )

        if response.status_code == 200:
            logging.info(f"Email succesfully sent to '{to}'")
            return True
        logging.error(
            f"Error when sending email\
            to '{to}' with error: {response.error}"
        )
        return False
