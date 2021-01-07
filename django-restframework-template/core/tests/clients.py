import json

from django.test import Client


class ApiClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None

    def get(self, *args, **kwargs):
        params = args[0].split('?')[1]

        kwargs.update({
            'content_type': 'application/json',
            'HTTP_X_MY_TOKEN': f'my_user {self.token}' if self.token else '',
        })
        rsp = super().get(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def post(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
            'HTTP_X_MY_TOKEN': f'my_user {self.token}' if self.token else '',
        })
        rsp = super().post(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def delete(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
            'HTTP_X_MY_TOKEN': f'my_user {self.token}' if self.token else '',
        })
        rsp = super().delete(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def put(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
            'HTTP_X_MY_TOKEN': f'my_user {self.token}' if self.token else '',
        })
        rsp = super().put(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def set_token(self, token):
        self.token = token
