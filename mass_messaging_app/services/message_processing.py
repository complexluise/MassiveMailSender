from jinja2 import Template
from mass_messaging_app.models.models import MessageCampaign, Contact


def render_message(template: MessageCampaign, contact: Contact) -> str:
    """
    Render a message from a campaigns with placeholders filled based on contact details.

    Parameters:
    - campaigns (MessageTemplate): The message campaigns with subject and body containing placeholders.
    - contact (Contact): The contact whose details will fill the campaigns's placeholders.

    Returns:
    - str: The rendered message body.
    """
    # Create a Jinja2 campaigns from the campaigns body
    jinja_template = Template(template.body)

    # Render the campaigns with data from the contact
    return jinja_template.render(**contact.dict())
