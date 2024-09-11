from typing import Optional

from d3m.domain import RootEntity
from pydantic import BaseModel

from ... import __domain_name__


class UserInfo(BaseModel):
    nickname: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    address: Optional[str] = None


class User(RootEntity, domain=__domain_name__):
    """
    RootEntity by default has reference as UUID.
    If custom reference type needed you can specify if by
    class User(RootEntity[CustomReferenceType], domain=__domain_name__).
    """
    login: str
    email: str
    passwd_hash: str
    verified: bool = False
    user_info: UserInfo
