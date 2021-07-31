import requests

from core.utils.hmac_signature import sign, verify


class UserBalanceVerifierFactory:
    CLIENT_TYPE_LOCAL = 100
    CLIENT_TYPE_REMOTE = 200

    @staticmethod
    def get_client(client_type):
        if client_type == UserBalanceVerifierFactory.CLIENT_TYPE_LOCAL:
            return LocalVerifier()
        elif client_type == UserBalanceVerifierFactory.CLIENT_TYPE_REMOTE:
            return RemoteVerifier()
        else:
            raise NotImplementedError


class IVerifier:

    def generate_hash(self, msg):
        raise NotImplementedError

    def is_verify(self, msg, signature_hash):
        raise NotImplementedError


class LocalVerifier(IVerifier):

    def __init__(self, secret_key='your_local_secret_key'):
        self.secret_key = secret_key

    def generate_hash(self, msg):
        return sign(self.secret_key, msg)

    def is_verify(self, msg, signature_hash):
        return verify(self.secret_key, msg, signature_hash)


class RemoteVerifier(IVerifier):

    def __init__(self, remote_url='http://127.0.0.1/', remote_api_key='', remote_secret_key=''):
        self.remote_url = remote_url
        self.remote_api_key = remote_api_key
        self.remote_secret_key = remote_secret_key

    def generate_hash(self, msg):
        data = {'msg': msg}
        headers = {'Content-Type': 'application/json'}
        url = self.remote_url + 'signature'
        rsp = requests.post(url, data=data, headers=headers)
        if rsp.status_code != 200 or 'hash' not in rsp.json():
            raise Exception(f'Remote verifier error, code = {rsp.status_code}, body = {rsp.content.decode()}')
        return rsp.json()['hash']

    def is_verify(self, msg, signature_hash):
        data = {'msg': msg, 'signature_hash': signature_hash}
        headers = {'Content-Type': 'application/json'}
        url = self.remote_url + 'signature/verify/'
        rsp = requests.post(url, data=data, headers=headers)
        if rsp.status_code != 200 or 'hash' not in rsp.json():
            raise Exception(f'Remote verifier error, code = {rsp.status_code}, body = {rsp.content.decode()}')
        return rsp.json()['success'] is True
