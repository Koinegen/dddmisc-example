from uuid import UUID

from d3m.domain import DomainEvent

from .. import __domain_name__


class BaseUserEvent(DomainEvent, domain=__domain_name__):
    pass


class UserCreatedAndVerified(BaseUserEvent):
    user_reference: UUID
