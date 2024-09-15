from d3m.domain import DomainError

from ...domain import __domain_name__


class BaseUserException(DomainError, domain=__domain_name__):
    example_kwargs: dict


class VerificationCodeIncorrect(BaseUserException):
    __template__ = "Incorrect verification code"


class AlreadyVerified(BaseUserException):
    __template__ = "Account already verified"
