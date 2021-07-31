from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction

from core.utils.datetime import get_datetime_format_iso8601, get_now_datetime_obj
from core.utils.formatter import format_to_decimal
from users.factory.user_balance_verify import UserBalanceVerifierFactory
from users.models import UserDetail, generate_salt
from users.services.user_balance import UserBalanceService


class UserService:

    @staticmethod
    def create_user_and_init(username):
        with transaction.atomic():
            # 建立User
            user = User.objects.create_user(username=username)

            # 初始化餘額, 算Hash
            time = get_now_datetime_obj()
            time_iso8601 = get_datetime_format_iso8601(time)
            new_balance = format_to_decimal(Decimal(0), 2)
            balance_hash_salt = generate_salt()
            msg = UserBalanceService._get_msg(time_iso8601, user.id, new_balance, balance_hash_salt)
            client = UserBalanceVerifierFactory.get_client(UserBalanceVerifierFactory.CLIENT_TYPE_LOCAL)
            balance_hash = client.generate_hash(msg)

            # 新增UserDetail
            UserDetail.objects.create(
                user=user,
                balance=new_balance,
                balance_hash_salt=balance_hash_salt,
                balance_hash=balance_hash,
                balance_update_at=time
            )
