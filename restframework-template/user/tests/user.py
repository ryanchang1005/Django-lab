import secrets

from core.tests.base import BaseTestCase
from core.utils.datetime import get_uts
from user.services.user import UserService


class UserAPITestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.EXIST_EMAIL = 'ryan@test.com'
        cls.EXIST_PASSWORD = secrets.token_urlsafe(10)

        UserService.create(
            email=cls.EXIST_EMAIL,
            password=cls.EXIST_PASSWORD
        )

    def _create_already_login_user(self, email):
        # pre data, create a user and set user token to headers
        data = {
            'uts': get_uts(),
            'email': email,
            'password': 'password123',
        }
        rsp = self.api_client.post('/api/user/', data=data)
        my_user = UserService.filter(api_key=rsp.json()['user_token']).first()
        self.api_client.set_token(my_user.api_key)
        return my_user

    def test_login_with_correct_email_and_password(self):
        # ready
        data = {
            'uts': get_uts(),
            'email': self.EXIST_EMAIL,
            'password': self.EXIST_PASSWORD,
        }

        # execute
        rsp = self.api_client.post('/api/user/login/', data=data)

        # assert
        self.assertEqual(rsp.status_code, 200)

        return_data = rsp.json()
        self.assertTrue('user_id' in return_data)
        self.assertTrue('user_token' in return_data)

    def test_create_user_with_not_exist_email(self):
        # ready
        data = {
            'uts': get_uts(),
            'email': 'ryan2@test.com',
            'password': 'password123',
        }

        # execute
        rsp = self.api_client.post('/api/user/', data=data)

        # assert
        self.assertEqual(rsp.status_code, 201)

        return_data = rsp.json()
        self.assertTrue('user_id' in return_data)
        self.assertTrue('user_token' in return_data)

    def test_logout_user(self):
        self._create_already_login_user('ryan3@test.com')

        # ready
        data = f'uts={get_uts()}'

        # execute
        rsp = self.api_client.delete(f'/api/user/logout/?{data}')

        # assert
        self.assertEqual(rsp.status_code, 204)

    def test_edit_user(self):
        my_user = self._create_already_login_user('ryan4@test.com')

        # ready
        data = {
            'uts': get_uts(),
            'display_name': 'new_name',
        }

        # execute
        rsp = self.api_client.put(f'/api/user/{my_user.id}/', data=data)

        # assert
        self.assertEqual(rsp.status_code, 200)

        return_data = rsp.json()
        self.assertTrue('display_name' in return_data)
