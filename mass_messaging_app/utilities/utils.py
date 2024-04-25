import json
import os

from jinja2 import Template
from mass_messaging_app.models.models import MessageCampaign, Contact


def render_message(template: MessageCampaign, contact: Contact) -> str:
    jinja_template = Template(template.body)
    return jinja_template.render(**contact.dict())


def load_message_campaign(json_file_path: str) -> MessageCampaign:
    """
    Load a message campaign from a JSON file. The JSON file contains metadata about the campaign,
    including a reference to an HTML file for the email body. The HTML file is assumed to be in the
    same directory as the JSON file.

    Args:
    json_file_path (str): The path to the JSON file containing the campaign configuration.

    Returns:
    MessageTemplate: A MessageTemplate instance with subject and body loaded from specified files.
    """
    directory = os.path.dirname(json_file_path)

    with open(json_file_path, "r", encoding="utf-8") as file:
        template_data = json.load(file)

    body_file_name = template_data.get("body_file")
    if body_file_name:
        body_file_path = os.path.join(directory, body_file_name)
        with open(body_file_path, "r", encoding="utf-8") as file:
            body_content = file.read()
        template_data["body"] = body_content
    else:
        template_data["body"] = ""

    body_file_name = template_data.get("body_file")
    if body_file_name:
        body_file_path = os.path.join(directory, body_file_name)
        with open(body_file_path, "r", encoding="utf-8") as body_file:
            body_content = body_file.read()
        template_data["body"] = body_content
    else:
        template_data["body"] = ""

    template_data.pop("body_file", None)

    attachment_file_name = template_data.get("attachment_file")
    if attachment_file_name:
        attachment_file_path = os.path.join(directory, attachment_file_name)
        with open(attachment_file_path, "rb") as attachment_file:
            attachment: bytes = attachment_file.read()
        template_data["attachment"] = attachment
        template_data["attachment_filename"] = os.path.basename(attachment_file_name)
    else:
        template_data["attachment"] = b''

    template_data.pop("attachment_file", None)

    return MessageCampaign(**template_data)
