from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from .models import models
from .config import settings
from jinja2 import Environment, select_autoescape, PackageLoader


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: models.User, url: str, email: List[EmailStr],):
        self.name = user.firstName
        self.sender = 'itsmurphy@yopmail.com'
        self.email = email
        self.url = url
        pass

    async def sendMail(self, subject, template):
        # Define the config
        conf = ConnectionConfig(
            MAIL_FROM_NAME='HireBlock',
            MAIL_USERNAME=settings.email_username,
            MAIL_PASSWORD=settings.email_password,
            MAIL_FROM=settings.email_from,
            MAIL_PORT=settings.email_port,
            MAIL_SERVER=settings.email_host,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=False
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            first_name=self.name,
            subject=subject
        )

        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def sendVerificationCode(self):
        await self.sendMail('Your verification code (Valid for 10min)', 'verification')
