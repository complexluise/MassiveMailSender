import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mass_messaging_app.models.models import Contact
from mass_messaging_app.config.settings import AppConfig


class EmailSender:
    """Class to handle email sending operations."""

    def __init__(self, config: AppConfig):
        self.config = config

    def send_email(self, contact: Contact, subject: str, html_message: str):
        """Sends an HTML email to a single recipient using Gmail SMTP service."""
        msg = MIMEMultipart()
        msg["From"] = self.config.smtp_user
        msg["To"] = contact.email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_message, "html"))

        try:
            with smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.smtp_use_ssl:
                    server.starttls()
                server.login(self.config.smtp_user, self.config.smtp_password)
                server.sendmail(self.config.smtp_user, contact.email, msg.as_string())
                print(f"Email sent successfully to {contact.email}")
        except smtplib.SMTPException as e:
            print(f"Failed to send email to {contact.email}. Error: {e}")


def setup_email_sender(smtp_settings) -> EmailSender:
    """Set up the email sender with configuration from settings."""
    return EmailSender(smtp_settings)
