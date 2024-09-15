from uuid import UUID

import pytest

from examples.users.user_svc.domain.model.exceptions import AlreadyVerified
from examples.users.user_svc.domain.model.user.entities import User, VerificationCodeIncorrect, UserInfo


class TestUserEntity:

    def test_user_creation(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        assert isinstance(user, User)
        assert user.login == 'user'
        assert user.email == 'user@test.com'
        assert user.passwd_hash == 'password'
        assert user.user_info == UserInfo()
        assert user.verified == False
        assert user.verification_code is None

    def test_generate_verification_code(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        generated_code = user.generate_verification_code()
        assert isinstance(generated_code, UUID)
        assert user.verification_code == generated_code

    def test_verify_fail_no_code_generated(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        with pytest.raises(VerificationCodeIncorrect):
            user.verify(UUID(int=123456789))
        assert not user.verified

    def test_verify_success(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        generated_code = user.generate_verification_code()
        user.verify(generated_code)
        assert user.verified
        assert user.verification_code is None
        assert next(user.collect_events()).__class__.__name__ == "UserCreatedAndVerified"

    def test_verify_fail_wrong_code(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        generated_code = user.generate_verification_code()
        with pytest.raises(VerificationCodeIncorrect):
            user.verify(UUID(int=123456789))
        assert not user.verified
        assert user.verification_code == generated_code

    def test_verify_fail_already_verified(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo())
        generated_code = user.generate_verification_code()
        user.verify(generated_code)
        assert user.verified
        assert user.verification_code is None
        with pytest.raises(VerificationCodeIncorrect):
            user.verify(generated_code)
        assert user.verified
        assert user.verification_code is None

    def test_generate_verification_code_verified_user(self):
        user = User(login='user',
                    email='user@test.com',
                    passwd_hash='password',
                    user_info=UserInfo(),
                    verified=True)

        with pytest.raises(AlreadyVerified):
            user.generate_verification_code()
