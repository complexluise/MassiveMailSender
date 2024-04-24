from csv import DictReader

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
        return _fetch_contacts_from_sheet(source_settings, spreadsheet_id, range_name)
    return []


def fetch_contacts_from_csv(file_path: str) -> list[Contact]:
    """
    Fetch contacts from a CSV file and convert them into a list of Contact models.

    Args:
    file_path (str): The path to the CSV file containing contact data.

    Returns:
    List[Contact]: A list of Contact model instances.
    """
    contacts = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader: DictReader = DictReader(file)
            for row in reader:
                # Assuming the CSV column names match the Contact model field names
                contact = Contact(**row)
                contacts.append(contact)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return contacts

