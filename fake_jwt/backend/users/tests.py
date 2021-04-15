import secrets

from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase

from core.tests.clients import ApiClient
from users.models import UserDetail

USERNAME = 'ryan'
PASSWORD = secrets.token_hex(10)


class UserAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with transaction.atomic():
            user = User.objects.create_user(
                username=USERNAME,
                password=PASSWORD
            )
            user_detail = UserDetail()
            user_detail.auth_user = user
            user_detail.save()
        cls.api_client = ApiClient()

    def test_login(self):
        api_client = ApiClient()

        data = {
            'username': USERNAME,
            'password': PASSWORD,
        }

        rsp = api_client.post('/api/users/login/', data=data)

        self.assertEqual(rsp.status_code, 200)
        return_data = rsp.json()
        self.assertTrue('user_id' in return_data)
        self.assertTrue('access_token' in return_data)

    def test_get_user_data(self):
        # login
        api_client = ApiClient()

        data = {
            'username': USERNAME,
            'password': PASSWORD,
        }

        rsp = api_client.post('/api/users/login/', data=data)

        self.assertEqual(rsp.status_code, 200)
        return_data = rsp.json()
        self.assertTrue('user_id' in return_data)
        self.assertTrue('access_token' in return_data)

        # get user data
        user_id = return_data['user_id']
        api_client = ApiClient(access_token=return_data['access_token'])
        rsp = api_client.get(f'/api/users/{user_id}/')

        self.assertEqual(rsp.status_code, 200)
        return_data = rsp.json()
        self.assertTrue('username' in return_data)
        self.assertTrue('last_login_at' in return_data)
