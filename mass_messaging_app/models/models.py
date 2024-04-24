from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class Contact(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    custom_fields: Optional[dict] = Field(default_factory=dict)
    # TODO add custom from sheets if is needed

class MessageTemplate(BaseModel):
    subject: str
    body: str

class AppConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    use_ssl: bool = True
