from mass_messaging_app.models.models import Contact
from mass_messaging_app.config.settings import GoogleServiceSettings
from mass_messaging_app.services.google_service import fetch_contacts_from_sheet


def fetch_contacts(
    source_type: str,
    source_settings: GoogleServiceSettings,
    spreadsheet_id: str,
    range_name: str,
) -> list[Contact]:
    if source_type == "google_sheets":
        return fetch_contacts_from_sheet(source_settings, spreadsheet_id, range_name)
    return []
