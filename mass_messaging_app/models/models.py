from typing import Optional

from pydantic import BaseModel, EmailStr, Extra


class Contact(BaseModel):
    email: EmailStr

    class Config:
        extra = Extra.allow  # Allows the model to accept arbitrary additional fields


class MessageCampaign(BaseModel):
    subject: str
    body: str
    attachment: bytes
    attachment_filename: Optional[str] = None
