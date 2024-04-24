import json
import os

from jinja2 import Template
from mass_messaging_app.models.models import MessageTemplate, Contact


def render_message(template: MessageTemplate, contact: Contact) -> str:
    jinja_template = Template(template.body)
    return jinja_template.render(**contact.dict())


def load_message_template(json_file_path: str) -> MessageTemplate:
    """
    Load a message template from a JSON file. The JSON file contains metadata about the campaign,
    including a reference to an HTML file for the email body. The HTML file is assumed to be in the
    same directory as the JSON file.

    Args:
    json_file_path (str): The path to the JSON file containing the campaign configuration.

    Returns:
    MessageTemplate: A MessageTemplate instance with subject and body loaded from specified files.
    """
    # Get the directory of the JSON file to ensure relative paths are handled correctly
    directory = os.path.dirname(json_file_path)

    # Load the JSON configuration
    with open(json_file_path, 'r', encoding='utf-8') as file:
        template_data = json.load(file)

    # Read the HTML content for the body from the specified file path
    body_file_name = template_data.get('body_file')
    if body_file_name:
        body_file_path = os.path.join(directory, body_file_name)
        with open(body_file_path, 'r', encoding='utf-8') as file:
            body_content = file.read()
        template_data['body'] = body_content
    else:
        # Default to an empty body if no file is specified
        template_data['body'] = ""

    # Remove the 'body_file' key as it's no longer needed and not expected by the MessageTemplate model
    template_data.pop('body_file', None)

    # Create and return the MessageTemplate instance
    return MessageTemplate(**template_data)

