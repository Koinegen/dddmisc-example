import abc


class AbstractMailAdapter(abc.ABC):

    @abc.abstractmethod
    async def send_email(self, email: str, subject: str, body: str):
        ...
