import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mass_messaging_app.models.models import Contact
from mass_messaging_app.config.settings import AppConfig


class EmailSender:
    """Class to handle email sending operations."""

    def __init__(self, config: AppConfig):
        self.config = config

    def send_email(self, contact: Contact, subject: str, message: str):
        """Sends an email to a single recipient."""
        msg = MIMEMultipart()
        msg["From"] = self.config.smtp_user
        msg["To"] = contact.email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_ssl:
                    server.starttls()
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.send_message(msg)
                print(f"Email sent successfully to {contact.email}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email to {contact.email}. Error: {e}")


def setup_email_sender(smtp_settings) -> EmailSender:
    """Set up the email sender with configuration from settings."""
    return EmailSender(smtp_settings)
