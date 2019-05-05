# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging


class Email:
    def __init__(self):
        try:
            self.sg_api = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        except Exception as e:
            logging.error("Sendgrid could not start!", e)

    def message(self, from_email, to_email, subject, body):
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=body)
        try:
            response = self.sg_api.send(message)
            logging.info(response.status_code)
            logging.info(response.body)
            logging.info(response.headers)
            return True
        except Exception as e:
            logging.error(e)
            return False
