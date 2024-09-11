from uuid import UUID

from .abstractions import AbstractMailAdapter
from .entities import User, UserInfo


class UserAggr:
    _mail_adapter: AbstractMailAdapter
    _user: User

    @classmethod
    def bootstrap(
            cls,
            mail_adapter: AbstractMailAdapter,
    ):
        cls._mail_adapter = mail_adapter

    @property
    def reference(self) -> UUID:
        return self._user.__reference__

    @classmethod
    def create(cls,
               login: str,
               email: str,
               passwd_hash: str) -> "UserAggr":
        _user = User(login=login,
                     email=email,
                     passwd_hash=passwd_hash,
                     user_info=UserInfo())
        obj = cls()
        obj._user = _user
        obj._user.create_event(
            "UserCreated",
            user_reference=obj._user.__reference__
        )
        return obj

    @classmethod
    def restore(cls) -> "UserAggr":
        ...

    async def send_verify_email(self):
        _subject = "Подтверждение регистрации"
        _body = """
        Some body with verify url
        """
        await self._mail_adapter.send_email(self._user.email, _subject, _body)
