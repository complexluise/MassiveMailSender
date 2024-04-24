import os
import argparse
from dotenv import load_dotenv
from tqdm import tqdm

from mass_messaging_app.config.settings import settings
from mass_messaging_app.models.models import Contact, MessageTemplate
from mass_messaging_app.services.data_source import (
    get_google_credentials,
    fetch_contacts_from_gsheets,
    fetch_contacts_from_csv,
)
from mass_messaging_app.services.message_processing import render_message
from mass_messaging_app.services.messenger import EmailSender, setup_email_sender
from mass_messaging_app.utilities.utils import load_message_template

load_dotenv()


def send_mail(contacts: list[Contact], template_path: str):
    template: MessageTemplate = load_message_template(template_path)
    email_sender: EmailSender = setup_email_sender(settings.smtp_settings)

    successes, failures = 0, 0

    with tqdm(total=len(contacts), desc="Sending Emails", unit="email") as progress_bar:
        for contact in contacts:
            try:
                message_body: str = render_message(template, contact)
                email_sender.send_email(contact, template.subject, message_body)
                successes += 1
            except Exception as error:
                print(f"Failed to send email to {contact.email}: {error}")
                failures += 1
            progress_bar.update(1)

    print(f"Email campaign completed: {successes} sent, {failures} failed.")


def main():

    parser = argparse.ArgumentParser(description="Mass Messaging App CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Sub-command for sending mail from CSV
    send_mail_csv = subparsers.add_parser("send_mail")
    send_mail_csv.add_argument(
        "--contacts_file",
        type=str,
        help="Path to the CSV file containing contacts.",
        required=False,
    )
    send_mail_csv.add_argument(
        "--spreadsheet_id",
        type=str,
        help="The ID of the Google Spreadsheet.",
        required=False,
    )
    send_mail_csv.add_argument(
        "--range_name",
        type=str,
        help="The range in the Google Spreadsheet to read.",
        required=False,
    )
    send_mail_csv.add_argument(
        "--msg_template",
        type=str,
        help="Path to the message template JSON file.",
        required=True,
    )

    # Sub-command for getting credentials
    get_creds = subparsers.add_parser("get_credentials")
    get_creds.add_argument(
        "--service",
        type=str,
        choices=["google"],
        help="Specify which service to get credentials for.",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "get_credentials" and args.service == "google":
        get_google_credentials()
    elif args.command == "send_mail":
        contacts: list[Contact] = []
        if args.contacts_file:
            contacts = fetch_contacts_from_csv(args.contacts_file)
        elif args.spreadsheet_id and args.range_name:
            contacts = fetch_contacts_from_gsheets(
                settings.google_settings, args.spreadsheet_id, args.range_name
            )
        else:
            parser.error(
                "Must specify either --contacts_file or both --spreadsheet_id and --range_name for send_mail."
            )
        send_mail(contacts, args.msg_template)


if __name__ == "__main__":
    """
    The command-line interface for the Mass Messaging App.

    This script allows you to send personalized emails to a list of contacts provided via a CSV file or directly from Google Sheets. To authenticate with Google services, you must first obtain the necessary credentials.

    Usage:

    To send emails to contacts listed in a CSV file:
    ```
    mass_messaging_app send_mail --contacts_file ./contacts/contacts.csv --msg_template ./templates/example.json
    ```

    To send emails to contacts from a Google Spreadsheet:
    ```
    mass_messaging_app send_mail --spreadsheet_id SPREADSHEET_ID --range_name RANGE_NAME --msg_template ./templates/example.json
    ```

    Before sending emails using Google Sheets as the source, ensure that you have obtained credentials:
    ```
    mass_messaging_app get_credentials --service google
    ```

    Arguments:
    --contacts_file      Path to the CSV file containing contacts.
    --spreadsheet_id     The ID of the Google Spreadsheet.
    --range_name         The range within the Google Spreadsheet to read contacts.
    --msg_template       Path to the JSON file that contains the email message template.

    Note: When using Google Sheets, --spreadsheet_id and --range_name must both be provided.
    """
    main()
