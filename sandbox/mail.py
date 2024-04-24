from google.cloud import gmail


def send_mass_mail(sender_email: str, recipient_emails: list, subject: str, body: str):
    """Sends a mass mail to a list of recipients.

    Args:
        sender_email (str): The email address of the sender.
        recipient_emails (list): A list of email addresses of the recipients.
        subject (str): The subject of the email.
        body (str): The body of the email.
    """

    client = gmail.GmailServiceClient()

    for recipient_email in recipient_emails:
        message = gmail.Message()
        message.subject = subject
        message.body = body

        mime_message = gmail.MimeMessage()
        mime_message.raw = message.to_json()

        message = client.create_draft(user_id="me", message=mime_message)

        client.send_message(user_id="me", message=message.id)


if __name__ == "__main__":
    send_mass_mail(
        "anadoriflame@gmail.com", ["luisehica@gmail.com"], "email_prueba", "it works"
    )
