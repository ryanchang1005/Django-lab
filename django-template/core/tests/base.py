from django.test import TestCase

from core.tests.clients import ApiClient


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_client = ApiClient()
