import json
from jinja2 import Template
from mass_messaging_app.models.models import MessageTemplate, Contact


def render_message(template: MessageTemplate, contact: Contact) -> str:
    jinja_template = Template(template.body)
    return jinja_template.render(**contact.dict())


def load_message_template(json_file_path: str) -> MessageTemplate:
    """Load message template from a JSON file."""
    with open(json_file_path, 'r') as file:
        template_data = json.load(file)
    return MessageTemplate(**template_data)
