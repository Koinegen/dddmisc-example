from examples.users.user_svc.domain.model.user.abstractions import AbstractMailAdapter
from examples.users.user_svc.domain.model.user.aggregate import UserAggr
from examples.users.user_svc.domain.model.user.entities import User, UserInfo


# Mock object for AbstractMailAdapter
class MockMailAdapter(AbstractMailAdapter):
    def __init__(self):
        self.subject = None
        self.body = None
        self.email = None

    async def send_email(self, email, subject, body):
        self.subject = subject
        self.body = body
        self.email = email


class TestUserAggregate:
    def test_user_aggr_bootstrap(self):
        mock_mail_adapter = MockMailAdapter()
        UserAggr.bootstrap(mock_mail_adapter, "example.com")
        assert UserAggr._mail_adapter is mock_mail_adapter
        assert UserAggr._verification_base_url == "example.com"

    def test_user_aggr_create(self):
        user_agg = UserAggr.create("login", "email@example.com", "passwd_hash")
        assert isinstance(user_agg, UserAggr)
        assert user_agg._user.login == "login"
        assert user_agg._user.email == "email@example.com"
        assert user_agg._user.passwd_hash == "passwd_hash"

    def test_user_aggr_restore(self):
        user = User(login="login", email="email@example.com", passwd_hash="passwd_hash", user_info=UserInfo())
        user_agg = UserAggr.restore(user)
        assert isinstance(user_agg, UserAggr)
        assert user_agg._user == user

    async def test_user_aggr_send_verify_email(self):
        mock_mail_adapter = MockMailAdapter()
        UserAggr.bootstrap(mock_mail_adapter, "example.com")
        user_agg = UserAggr.create("login", "email@example.com", "passwd_hash")
        await user_agg.send_verify_email()
        assert mock_mail_adapter.subject == "Подтверждение регистрации"
        assert "https://example.com/verify_mail?user={}&code=".format(user_agg.reference) in mock_mail_adapter.body
        assert mock_mail_adapter.email == "email@example.com"
