from django.test import Client


class ApiClient(Client):

    def __init__(self, access_token=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = access_token

    def get(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.access_token:
            kwargs.update({
                'Authorization': f'Bearer {self.access_token}'
            })
        rsp = super().get(*args, **kwargs)
        print(rsp.content.decode())
        return rsp

    def post(self, *args, **kwargs):
        kwargs.update({
            'content_type': 'application/json',
        })

        if self.access_token:
            kwargs.update({
                'Authorization': f'Bearer {self.access_token}'
            })
        rsp = super().post(*args, **kwargs)
        print(rsp.content.decode())
        return rsp
