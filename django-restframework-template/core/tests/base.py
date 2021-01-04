import secrets

from django.test import TestCase

from core.tests.clients import ApiClient
from user.services.user import UserService


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_client = ApiClient()


class BaseUserTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        my_user = UserService.create(
            email='ryan@test.com',
            password=secrets.token_urlsafe(10)
        )

        cls.api_client = ApiClient()
        cls.api_client.set_token(token=my_user.api_key)
