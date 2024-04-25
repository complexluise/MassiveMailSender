import time
import argparse
from dotenv import load_dotenv
from tqdm import tqdm

from mass_messaging_app.config.settings import settings
from mass_messaging_app.models.models import Contact, MessageCampaign
from mass_messaging_app.services.data_source import (
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
                email_sender.send_email(
                    contact,
                    campaign.subject,
                    message_body,
                    campaign.attachment,
                    campaign.attachment_filename,
                )
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
        required=True,
    )
    send_mail_csv.add_argument(
        "--campaign",
        type=str,
        help="Path to the message campaign JSON file.",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "send_mail":
        contacts: list[Contact] = []
        if args.contacts_file:
            contacts = fetch_contacts_from_csv(args.contacts_file)
        else:
            parser.error("Must specify either --contacts_file")
        send_mail(contacts, args.campaign)


if __name__ == "__main__":
    """
    The command-line interface for the Mass Messaging App.

    This script allows you to send personalized emails to a list of contacts provided via a CSV file.

    Usage:

    To send emails to contacts listed in a CSV file:
    ```
    mass_messaging_app send_mail --contacts_file ./contacts/contacts.csv --campaign ./campaigns/example.json
    ```

    Arguments:
    --contacts_file  Path to the CSV file containing contacts.
    --campaign       Path to the JSON file that contains the email message campaign.

    """
    main()
