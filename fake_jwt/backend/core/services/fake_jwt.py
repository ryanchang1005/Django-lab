import time
import jwt

from core.settings import JWT_SECRET_KEY


class FakeJWTService:

    @staticmethod
    def generate_access_token(user):
        now = int(time.time() * 1000)
        exp = now + (1 * 24 * 60 * 60 * 1000)  # 1 day
        data = {
            'user_id': user.userdetail.pub_id,
            'exp': exp,
        }
        encoded_jwt = jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decode_access_token_data(access_token):
        try:
            return jwt.decode(access_token, JWT_SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return None

    @staticmethod
    def is_access_token_valid(access_token):
        val = FakeJWTService.decode_access_token_data(access_token)
        # 簽章無效
        if not val:
            return False

        exp = val['exp']
        now = int(time.time() * 1000)

        # 過期
        if now > exp:
            return False

        return True
