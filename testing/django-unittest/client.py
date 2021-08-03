import hmac
import json

from django.test import Client


class ApiClient(Client):

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def get(self, *args, **kwargs):
        payload = args[0].split('?')[1]
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.api_token:
            kwargs.update({
                'HTTP_X_XXX_TOKEN': '',
                'HTTP_X_XXX_SIGNATURE': '',
            })
        rsp = super().get(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def post(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.api_token:
            kwargs.update({
                'HTTP_X_XXX_TOKEN': '',
                'HTTP_X_XXX_SIGNATURE': '',
            })
        rsp = super().post(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def put(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.api_token:
            kwargs.update({
                'HTTP_X_XXX_TOKEN': '',
                'HTTP_X_XXX_SIGNATURE': '',
            })
        rsp = super().put(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def delete(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.api_token:
            kwargs.update({
                'HTTP_X_XXX_TOKEN': '',
                'HTTP_X_XXX_SIGNATURE': '',
            })
        rsp = super().delete(*args, **kwargs)
        print(rsp.content.decode())
        return rsp
