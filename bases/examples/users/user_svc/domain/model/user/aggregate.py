from uuid import UUID

from .abstractions import AbstractMailAdapter
from .entities import User, UserInfo


class UserAggr:
    _mail_adapter: AbstractMailAdapter
    _verification_base_url: str
    _user: User

    @classmethod
    def bootstrap(
            cls,
            mail_adapter: AbstractMailAdapter,
            verification_base_url: str,
    ):
        cls._mail_adapter = mail_adapter
        cls._verification_base_url = verification_base_url

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
            'UserCreated',
            user_reference=_user.__reference__
        )

        return obj

    @classmethod
    def restore(cls, user: User) -> "UserAggr":
        obj = cls()
        obj._user = user
        return obj

    async def send_verify_email(self):
        code = self._user.generate_verification_code()
        subject = "Подтверждение регистрации"
        body = f"""
        Verification link: 
        https://{self._verification_base_url}/verify_mail?user={self._user.__reference__}&code={code}
        """
        await self._mail_adapter.send_email(self._user.email, subject, body)
