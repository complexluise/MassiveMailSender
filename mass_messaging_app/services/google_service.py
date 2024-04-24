import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from mass_messaging_app.models.models import Contact
from mass_messaging_app.models.constants import SCOPES
from mass_messaging_app.config.settings import GoogleServiceSettings


def _get_credentials_from_oauth():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


def _get_service(credentials_path: str, scopes: list[str]):
    """Create a Google Sheets service client."""
    credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    service = build("sheets", "v4", credentials=credentials)
    return service


def _fetch_contacts_from_sheet(
    settings: GoogleServiceSettings, spreadsheet_id: str, range_name: str
) -> list[Contact]:
    """Fetch contacts from a Google Sheet and return a list of Contact models."""
    service = _get_service(
        settings.google_credentials_path,
        ["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    sheet = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    values = sheet.get("values", [])
    contacts = [
        Contact(name=row[0], email=row[1], phone=row[2])
        for row in values
        if len(row) >= 3
    ]
    # TODO esto puede fallar porque esta parseando la primer linea
    return contacts
