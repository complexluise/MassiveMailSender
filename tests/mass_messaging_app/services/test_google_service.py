from mass_messaging_app.config.settings import GoogleServiceSettings
from mass_messaging_app.models.models import Contact
from mass_messaging_app.services.google_service import (
    _get_credentials_from_oauth,
    _get_service,
    _fetch_contacts_from_sheet,
)


def test__fetch_contacts_from_sheet():
    settings = GoogleServiceSettings()
    contacts: list[Contact] = _fetch_contacts_from_sheet(
        settings=settings, spreadsheet_id="123", range_name="A1:B3"
    )
    assert len(contacts) > 0
