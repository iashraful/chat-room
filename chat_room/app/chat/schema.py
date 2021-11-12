from typing import List, Optional
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class GroupCreateSchema(BaseModel):
    group_name: str
    logo: Optional[str]
    subscribers: List[EmailStr]
    moderators: Optional[List[EmailStr]]
