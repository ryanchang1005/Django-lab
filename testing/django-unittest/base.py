import json
import secrets

from django.test import TestCase

from core.services.init import InitService

class BaseAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # initialize some default value
        InitService.init_permission()
        InitService.init_role()
        InitService.some_init()

        # create a test user
        user = User.objects.create_user(username='ryan', password=secrets.token_hex(20))
        cls.BASE_USER = user
        cls.api_client_unlogin = ApiClient()
        cls.api_client = ApiClient(user)

class MockResponse:
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.status_code = status_code
        self.content = json.dumps(json_data).encode()
        self.headers = headers

    def json(self):
        return self.json_data