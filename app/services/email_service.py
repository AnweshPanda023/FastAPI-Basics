import smtplib
from email.message import EmailMessage

from app.core.config import settings


class EmailService:

    def send_password_reset_email(
        self,
        email: str,
        reset_token: str,
    ) -> None:

        reset_url = (
            f"{settings.frontend_url}" f"/reset-password" f"?token={reset_token}"
        )

        message = EmailMessage()

        message["From"] = settings.email_from
        message["To"] = email
        message["Subject"] = "Reset your password"

        message.set_content(f"""
Password Reset

We received a request to reset your password.

Click the link below to reset your password:

{reset_url}

This link expires in 30 minutes.

If you did not request this password reset,
you can safely ignore this email.
""")

        with smtplib.SMTP(
            settings.smtp_host,
            settings.smtp_port,
        ) as smtp:

            if settings.smtp_username and settings.smtp_password:
                # smtp.starttls() #uncomment to use real gmail
                smtp.login(
                    settings.smtp_username,
                    settings.smtp_password,
                )

            smtp.send_message(message)
