import logging
import random

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LogMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        self.fake_data(request, response)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def fake_data(self, request, response):
        ip = self.get_client_ip(request)

        for i in range(random.randint(500, 1500)):
            logger.info(f'ip: {ip}, '
                        f'method: {self.get_fake_method()}, '
                        f'url: {self.get_fake_url()}, '
                        f'status_code: {self.get_fake_status_code()}')

    def get_fake_status_code(self):
        return random.choice([200, 201, 204, 400, 401, 403, 404, 429, 500, 502, 504])

    def get_fake_url(self):
        urls = []
        urls += ['/users/', '/users/1/', '/users/1/xxx']
        urls += ['/orders/', '/orders/1/', '/orders/1/xxx']
        urls += ['/posts/', '/posts/1/', '/posts/1/xxx']
        urls += ['/books/', '/books/1/', '/books/1/xxx']
        urls += ['/chats/', '/chats/1/', '/chats/1/xxx']
        return random.choice(urls)

    def get_fake_method(self):
        return random.choice(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
