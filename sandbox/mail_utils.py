import base64
import os
from dotenv import load_dotenv
from email.message import EmailMessage

import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


def gmail_send_message(to_mail: str, from_mail: str, subject: str, mail_content: str) -> None:
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  
  creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=SCOPES,
                subject="anadoriflame@gmail.com")

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(mail_content)

    message["To"] = to_mail
    message["From"] = from_mail
    message["Subject"] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
  gmail_send_message("luisehica@gmail.com", "anadoriflame@gmail.com", "hola", "mensaje automatico")