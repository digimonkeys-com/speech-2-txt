import os

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_TLS=os.getenv('MAIL_TLS'),
    MAIL_SSL=os.getenv('MAIL_SSL'),
    USE_CREDENTIALS=os.getenv('USE_CREDENTIALS'),
    VALIDATE_CERTS=os.getenv('VALIDATE_CERTS')
)


async def send_email_reset_password(email: list, reset_code: str):
    reset_subject = "Reset password to Digimonkeys"
    recipient = email
    msg = f"""
        Someone requested a link to reset your password. If it wasn't you, please ignore this email.
        
        http://localhost:8000/reset-password?reset_token={reset_code}
        
        Your password won't change until you access the link and create a new one.
        The link has expiry time so do not wait to long to hit it!
    """

    message = MessageSchema(
        subject=reset_subject,
        recipients=recipient,
        body=msg
    )

    fm = FastMail(conf)
    await fm.send_message(message)
