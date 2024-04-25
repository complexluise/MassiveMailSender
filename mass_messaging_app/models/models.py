from pydantic import BaseModel, EmailStr, Extra


class Contact(BaseModel):
    email: EmailStr

    class Config:
        extra = Extra.allow  # Allows the model to accept arbitrary additional fields


class MessageCampaign(BaseModel):
    subject: str
    body: str
    attachment: bytes
    attachment_filename: str


class AppConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    use_ssl: bool = True
