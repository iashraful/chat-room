from typing import Dict, List, Optional
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class Group(BaseModel):
    group_name: str
    logo: Optional[str]
    subscribers: List[EmailStr]
    admin: dict
    moderators: Optional[List[EmailStr]]

    @classmethod
    def collection_name(cls):
        return "groups"


class GroupChat(BaseModel):
    group_id: str
    sender: EmailStr
    msg: str

    @classmethod
    def collection_name(cls):
        return "group_chats"


class Inbox(BaseModel):
    logo: Optional[str]
    access_key: str  # We will generate the access_key from subscribers user id
    subscribers: List[EmailStr]

    @classmethod
    def collection_name(cls):
        return "inboxes"


class InboxChat(BaseModel):
    inbox_id: str
    sender: EmailStr
    receiver: EmailStr
    msg: str

    @classmethod
    def collection_name(cls):
        return "inbox_chats"
