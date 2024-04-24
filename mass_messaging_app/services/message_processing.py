from jinja2 import Template
from mass_messaging_app.models.models import MessageTemplate, Contact


def render_message(template: MessageTemplate, contact: Contact) -> str:
    """
    Render a message from a template with placeholders filled based on contact details.

    Parameters:
    - template (MessageTemplate): The message template with subject and body containing placeholders.
    - contact (Contact): The contact whose details will fill the template's placeholders.

    Returns:
    - str: The rendered message body.
    """
    # Create a Jinja2 template from the template body
    jinja_template = Template(template.body)

    # Render the template with data from the contact
    return jinja_template.render(**contact.dict())
