from pydantic import ValidationError

from src.models import Contact

def parse_values_into_pydantic(data: list) -> list[Contact]:
    headers: list = data[0]
    rows: list = data[1:]

    # Convert the list of lists into list of dicts using headers
    data_dicts: list[dict] = [{headers[i]: value for i, value in enumerate(row)} for row in rows]

    # Create Pydantic models from dicts
    contacts: list = []
    for row_dict in data_dicts:
        try:
            contact: Contact = Contact.parse_obj(row_dict)
            contacts.append(contact)
        except ValidationError as e:
            print("Data validation error:", e)

    return contacts
