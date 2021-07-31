from django.db import transaction

from core.utils.datetime import get_datetime_format_iso8601, get_now_datetime_obj
from core.utils.formatter import format_to_decimal
from users.factory.user_balance_verify import UserBalanceVerifierFactory
from users.models import UserDetail, UserBalanceLog


class UserBalanceService:

    @staticmethod
    def _get_msg_by_user_detail(user_detail):
        balance = user_detail.balance
        time_iso8601 = get_datetime_format_iso8601(user_detail.balance_update_at)
        return UserBalanceService._get_msg(
            time_iso8601, user_detail.user.id, format_to_decimal(balance, 2), user_detail.balance_hash_salt
        )

    @staticmethod
    def _get_msg(time_iso8601, user_id, balance, salt):
        return f'{time_iso8601}.{user_id}.{balance}.{salt}'

    @staticmethod
    def get_balance(user_detail):
        msg = UserBalanceService._get_msg_by_user_detail(user_detail)
        client = UserBalanceVerifierFactory.get_client(UserBalanceVerifierFactory.CLIENT_TYPE_LOCAL)
        is_verify = client.is_verify(msg, user_detail.balance_hash)
        if is_verify is False:
            raise Exception(
                f'is_verify = {is_verify}, '
                f'username = {user_detail.user.username}, '
                f'balance = {user_detail.balance}, '
                f'balance_hash = {user_detail.balance_hash}'
            )
        return user_detail.balance

    @staticmethod
    def increase_balance(user_detail, amount):
        if amount <= 0:
            raise Exception('Can not be negative')
        UserBalanceService._update_balance(user_detail, amount)

    @staticmethod
    def decrease_balance(user_detail, amount):
        if amount <= 0:
            raise Exception('Can not be negative')
        UserBalanceService._update_balance(user_detail, -amount)

    @staticmethod
    def _update_balance_with_lock(user_detail, amount):
        """
        悲觀鎖
        """
        with transaction.atomic():
            user_detail = UserDetail.objects.select_for_update().get(id=user_detail.id)
            user = user_detail.user

            # 取得餘額並驗證
            balance = UserBalanceService.get_balance(user_detail)

            # 新餘額
            new_balance = balance + amount

            # 檢查餘額足夠
            if new_balance < 0:
                raise Exception('balance not enough')

            # 產生新的Hash(time, user id, 新餘額, salt)
            time = get_now_datetime_obj()
            time_iso8601 = get_datetime_format_iso8601(time)
            msg = UserBalanceService._get_msg(
                time_iso8601, user.id, format_to_decimal(new_balance, 2), user_detail.balance_hash_salt
            )
            client = UserBalanceVerifierFactory.get_client(UserBalanceVerifierFactory.CLIENT_TYPE_LOCAL)
            new_balance_hash = client.generate_hash(msg)

            user_detail.balance = new_balance
            user_detail.balance_hash = new_balance_hash
            user_detail.balance_update_at = time
            user_detail.save(update_fields=['balance', 'balance_hash', 'balance_update_at'])

            UserBalanceLog.objects.create(
                user=user,
                amount=new_balance - balance,
                from_balance=balance,
                to_balance=new_balance,
                created=time,
            )

    @staticmethod
    def _update_balance(user_detail, amount):
        """
        樂觀鎖
        """
        with transaction.atomic():
            user = user_detail.user

            # 取得餘額並驗證
            balance = UserBalanceService.get_balance(user_detail)

            # 新餘額
            new_balance = balance + amount

            # 檢查餘額足夠
            if new_balance < 0:
                raise Exception('balance not enough')

            # 產生新的Hash(time, user id, 新餘額, salt)
            time = get_now_datetime_obj()
            time_iso8601 = get_datetime_format_iso8601(time)
            msg = UserBalanceService._get_msg(
                time_iso8601, user.id, format_to_decimal(new_balance, 2), user_detail.balance_hash_salt
            )
            client = UserBalanceVerifierFactory.get_client(UserBalanceVerifierFactory.CLIENT_TYPE_LOCAL)
            new_balance_hash = client.generate_hash(msg)

            ret = UserDetail.objects.filter(
                user=user,
                balance=balance,
                balance_hash=user_detail.balance_hash,
            ).update(
                balance=new_balance,
                balance_hash=new_balance_hash,
                balance_update_at=time,
            )

            if ret != 1:
                raise Exception('Update balance error')

            UserBalanceLog.objects.create(
                user=user,
                amount=new_balance - balance,
                from_balance=balance,
                to_balance=new_balance,
                created=time,
            )

"""
from users.services.user import *
from users.services.user_balance import *
from core.utils.datetime import *

print(f'start balance = {UserDetail.objects.first().balance}, {get_now_datetime_obj()}')
for _ in range(1000):
    UserBalanceService.increase_balance(UserDetail.objects.first(), Decimal(1))

print(f'end balance = {UserDetail.objects.first().balance}, {get_now_datetime_obj()}')
"""
