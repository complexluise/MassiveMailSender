import os
import argparse
from dotenv import load_dotenv

from mass_messaging_app.config.settings import settings
from mass_messaging_app.models.models import Contact, MessageTemplate
from mass_messaging_app.services.data_source import fetch_contacts
from mass_messaging_app.services.message_processing import render_message
from mass_messaging_app.services.messenger import EmailSender, setup_email_sender
from mass_messaging_app.utilities.utils import load_message_template

load_dotenv()


def main(spreadsheet_id: str, range_name: str, template_path: str):

    contacts: list[Contact] = fetch_contacts(
        source_type="google_sheets",
        source_settings=settings.google_settings,
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
    )

    template: MessageTemplate = load_message_template(template_path)

    email_sender: EmailSender = setup_email_sender(smtp_settings=settings.smtp_settings)

    for contact in contacts:
        rendered_message = render_message(template, contact)
        email_sender.send_email(contact, template.subject, rendered_message)
        print(f"Email sent to {contact.email}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Send personalized emails to contacts from a Google Sheet."
    )
    parser.add_argument(
        "--spreadsheet_id",
        type=str,
        help="The ID of the Google Spreadsheet.",
        required=True,
    )
    parser.add_argument(
        "--range_name",
        type=str,
        help="The range in the Google Spreadsheet to read.",
        required=True,
    )
    parser.add_argument(
        "--msg_template",
        type=str,
        help="Template of the msg to send, be carefull use the same variables as the google sheets", # TODO check grammar
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(spreadsheet_id=os.getenv("SPREADSHEET_ID"), range_name="A1:B2")
    # args = parse_args()
    # main(spreadsheet_id=args.spreadsheet_id, range_name=args.range_name, template_path= args.msg_template)
