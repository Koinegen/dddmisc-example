import abc
from uuid import UUID

from d3m.hc import HandlersCollection
from d3m.uow import UnitOfWorkBuilder

from ..model import commands as cmd
from ..model.user.aggregate import UserAggr


class AbstractUserRepository(abc.ABC):

    @abc.abstractmethod
    def create_user(self, login: str, email: str, passwd_hash: str) -> UserAggr:
        ...

    @abc.abstractmethod
    async def get_user(self, user_reference: UUID):
        ...


user_collection = HandlersCollection()


@user_collection.register
async def create_user(
        command: cmd.CreateUserCommand,
        uow_builder: UnitOfWorkBuilder[AbstractUserRepository],
):
    async with uow_builder() as uow:
        user_aggr = uow.repository.create_user(
            login=command.login,
            email=command.email,
            passwd_hash=command.passwd_hash,
        )
        await uow.apply()
    return user_aggr.reference


@user_collection.register
async def verify_user(
        command: cmd.VerifyUserCommand,
        uow_builder: UnitOfWorkBuilder[AbstractUserRepository],
):
    async with uow_builder() as uow:
        user_aggr = await uow.repository.get_user(user_reference=command.user_reference)
        await user_aggr.send_verify_email()
        await uow.apply()


@user_collection.subscribe('user.service.UserCreated')
@user_collection.register
async def send_verification_code(
        command: cmd.SendVerificationCodeCommand,
        uow_builder: UnitOfWorkBuilder[AbstractUserRepository],
):
    async with uow_builder() as uow:
        user_aggr = await uow.repository.get_user(
            user_reference=command.user_reference
        )
        await user_aggr.send_verify_email()
        await uow.apply()
