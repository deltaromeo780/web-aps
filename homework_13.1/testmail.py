import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


async def send_in_background():
    try:
        conf = ConnectionConfig(
            MAIL_USERNAME="pawel.czerwinski78@gmail.com",
            MAIL_PASSWORD="hpqj iezo jvyi kehk",
            MAIL_FROM="pawel.czerwinski78@gmail.com",
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_FROM_NAME="Example email",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        message = MessageSchema(
            subject="Fastapi mail module",
            recipients=["deltaromeodev@gmail.com"],
            body="first test mail",
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        print("Email został pomyślnie wysłany.")
    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania emaila: {e}")


asyncio.run(send_in_background())
