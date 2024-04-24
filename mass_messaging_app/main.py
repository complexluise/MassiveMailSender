import os
import argparse
from dotenv import load_dotenv

from mass_messaging_app.config.settings import settings
from mass_messaging_app.models.models import Contact, MessageTemplate
from mass_messaging_app.services.data_source import (
    get_google_credentials,
    fetch_contacts_from_gsheets,
    fetch_contacts_from_csv
)
from mass_messaging_app.services.message_processing import render_message
from mass_messaging_app.services.messenger import EmailSender, setup_email_sender
from mass_messaging_app.utilities.utils import load_message_template

load_dotenv()


def send_mail(contacts: list[Contact], template_path: str):
    template: MessageTemplate = load_message_template(template_path)

    email_sender: EmailSender = setup_email_sender(smtp_settings=settings.smtp_settings)

    for contact in contacts:
        rendered_message = render_message(template, contact)
        email_sender.send_email(contact, template.subject, rendered_message)
        print(f"Email sent to {contact.email}")


def main():

    parser = argparse.ArgumentParser(description="Mass Messaging App CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Sub-command for sending mail from CSV
    send_mail_csv = subparsers.add_parser('send_mail')
    send_mail_csv.add_argument('--contacts_file', type=str, help='Path to the CSV file containing contacts.', required=False)
    send_mail_csv.add_argument('--spreadsheet_id', type=str, help='The ID of the Google Spreadsheet.', required=False)
    send_mail_csv.add_argument('--range_name', type=str, help='The range in the Google Spreadsheet to read.', required=False)
    send_mail_csv.add_argument('--msg_template', type=str, help='Path to the message template JSON file.', required=True)

    # Sub-command for getting credentials
    get_creds = subparsers.add_parser('get_credentials')
    get_creds.add_argument('--service', type=str, choices=['google'], help='Specify which service to get credentials for.', required=True)

    args = parser.parse_args()

    if args.command == 'get_credentials' and args.service == 'google':
        get_google_credentials()
    elif args.command == 'send_mail':
        contacts: list[Contact] = []
        if args.contacts_file:
            contacts = fetch_contacts_from_csv(args.contacts_file)  # TODO aquí puede haber un error.
        elif args.spreadsheet_id and args.range_name:
            contacts = fetch_contacts_from_gsheets(settings.google_settings, args.spreadsheet_id, args.range_name)
        else:
            parser.error("Must specify either --contacts_file or both --spreadsheet_id and --range_name for send_mail.")
        send_mail(contacts, args.msg_template)


if __name__ == "__main__":
    main(spreadsheet_id=os.getenv("SPREADSHEET_ID"), range_name="A1:B2")
    # args = parse_args()
    # main(spreadsheet_id=args.spreadsheet_id, range_name=args.range_name, template_path= args.msg_template)
