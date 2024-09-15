import uuid
from typing import Optional
from uuid import UUID

from d3m.domain import RootEntity
from pydantic import BaseModel

from ..exceptions import VerificationCodeIncorrect, AlreadyVerified
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
    verification_code: Optional[UUID] = None
    user_info: UserInfo

    def generate_verification_code(self) -> UUID:
        if self.verified:
            raise AlreadyVerified()
        self.verification_code = uuid.uuid4()
        return self.verification_code

    def verify(self, code: UUID):
        if code == self.verification_code and self.verification_code:
            self.verified = True
            self.verification_code = None
            self.create_event(
                "UserCreatedAndVerified",
                user_reference=self.__reference__
            )
        else:
            raise VerificationCodeIncorrect()
