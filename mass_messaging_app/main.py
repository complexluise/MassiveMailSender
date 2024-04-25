import time
import argparse
from dotenv import load_dotenv
from tqdm import tqdm

from mass_messaging_app.config.settings import settings
from mass_messaging_app.models.models import Contact, MessageCampaign
from mass_messaging_app.services.data_source import (
    get_google_credentials,
    fetch_contacts_from_gsheets,
    fetch_contacts_from_csv,
)
from mass_messaging_app.services.message_processing import render_message
from mass_messaging_app.services.messenger import EmailSender, setup_email_sender
from mass_messaging_app.utilities.utils import load_message_campaign

load_dotenv()


def send_mail(contacts: list[Contact], campaign_path: str):
    campaign: MessageCampaign = load_message_campaign(campaign_path)
    email_sender: EmailSender = setup_email_sender(settings.smtp_settings)

    successes, failures = 0, 0

    with tqdm(total=len(contacts), desc="Sending Emails", unit="email") as progress_bar:
        for contact in contacts:
            try:
                time.sleep(0.1)
                message_body: str = render_message(campaign, contact)
                email_sender.send_email(contact, campaign.subject, message_body, campaign.attachment, campaign.attachment_filename)
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
        "--campaign",
        type=str,
        help="Path to the message campaign JSON file.",
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
        send_mail(contacts, args.campaign)


if __name__ == "__main__":
    """
    The command-line interface for the Mass Messaging App.

    This script allows you to send personalized emails to a list of contacts provided via a CSV file or directly from Google Sheets. To authenticate with Google services, you must first obtain the necessary credentials.

    Usage:

    To send emails to contacts listed in a CSV file:
    ```
    mass_messaging_app send_mail --contacts_file ./contacts/contacts.csv --campaign ./campaigns/example.json
    ```

    To send emails to contacts from a Google Spreadsheet:
    ```
    mass_messaging_app send_mail --spreadsheet_id SPREADSHEET_ID --range_name RANGE_NAME --campaign ./campaigns/example.json
    ```

    Before sending emails using Google Sheets as the source, ensure that you have obtained credentials:
    ```
    mass_messaging_app get_credentials --service google
    ```

    Arguments:
    --contacts_file      Path to the CSV file containing contacts.
    --spreadsheet_id     The ID of the Google Spreadsheet.
    --range_name         The range within the Google Spreadsheet to read contacts.
    --campaign       Path to the JSON file that contains the email message campaign.

    Note: When using Google Sheets, --spreadsheet_id and --range_name must both be provided.
    """
    main()
