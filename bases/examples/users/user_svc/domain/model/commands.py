from uuid import UUID

from d3m.domain import DomainCommand

from .. import __domain_name__


class BaseUserCommand(DomainCommand, domain=__domain_name__):
    pass


class CreateUserCommand(BaseUserCommand):
    login: str
    email: str
    passwd_hash: str


class SendVerificationCodeCommand(BaseUserCommand):
    user_reference: UUID
