"""
My Django API, flow

                                                        <> UserDBRepository
UserViewSet(Serializer) <> UserService <> UserRepository
                                                        <> UserCacheRepository

core
   services
        init.py
        redis.py
        aws_s3.py
        aws_ses.py
        third_party_sms.py
        third_party_api1.py
        third_party_api2.py
users
   views
       users.py
    services
       users.py
    serializers
       users.py
    repositories
       users.py
    tests
       users.py
    models.py
system
taskapp

"""


class UserViewSet:

    def login(self, request):
        clean_data = UserLoginSerializer(
            request.data).get_validate_data(request.data)
        return UserService.login(clean_data)


class UserLoginSerializer:
    def get_validate_data(data):
        # check format(str length, int (min, max), url format, phone number format)
        # convert to object(time)
        # decrypt(password encrypt from frontend)
        pass


class UserService:

    @staticmethod
    def login(data):
        # check user info from DB(username, password, is_active)
        user = UserRepository.get(data['username'], with_cache=False)
        if not user.check_password(data['password']):
            raise Exception('Invalid username or password')

        # send login notify(email, sms)
        MessageNotifyService.send(user)

        # set user info to cache(redis)
        UserRepository.set_user_cache(user)

        return user


class UserRepository:

    def __init__(self, user_db_repository, user_cache_repository):
        self.user_db_repository = user_db_repository
        self.user_cache_repository = user_cache_repository

    def get_user_cache_template(user):
        return {
            'id': user.id,
            'username': user.username,
            'api_token': user.api_token,
        }

    def get(username, with_cache=True):
        if with_cache is True:
            user_cache_data = self.user_cache_repository.get(username)
            if user_cache_data:
                return user_cache_data  # dict
            else:
                user = user_db_repository.get(username)
                user_cache_data = self.get_user_cache_template(user)

                # can be optimize(by MQ)
                self.user_cache_repository.set_user_detail(
                    username, user_cache_data)
                return user_cache_data  # dict
        else:
            return user_db_repository.get(username)  # Model

    def set_user_cache(user):
        user_cache_data = self.get_user_cache_template(user)  # dict
        self.user_cache_repository.set_user_detail(
            user.username, user_cache_data)

    def get_user_cache(user):
        return self.user_cache_repository.get(user.username)


class UserDBRepository:

    def get(qs=None, username=None):
        if qs is None:
            qs = User.object.all()

        if not is_empty(username):
            qs = qs.filter(username=username)
        return qs


class UserCacheRepository:

    def __init__(self, redis_service):
        self.redis_service = redis_service

    def _get_user_detail_key(username):
        hash_value = hash(username)
        return f'user.detail.{hash_value}'

    def get_user_detail(username):
        key = self._get_user_detail_key(username)
        return self.redis_service.hgetall(key)

    def set_user_detail(username, data):
        key = self._get_user_detail_key(username)
        self.redis_service.hmset(key, data, timeout='1H')


"""
# OtherService/Utils
RedisService(Redis)
MessageNotifyService(封裝Email & SMS)(
    AWSSESService(Email), ThirdPartySMSService(SMS)
)
AWSS3Service(Object storage)
"""
