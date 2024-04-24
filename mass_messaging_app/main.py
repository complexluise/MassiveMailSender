from src.extract_sheet import extract_values_from_sheets



values = extract_values_from_sheets()
contacts = parse_values_into_pydantic(values)
for contact in contacts:
    send_mail(contact)