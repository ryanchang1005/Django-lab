import secrets

from core.tests.base import BaseTestCase, BaseUserTestCase
from core.utils.datetime import get_uts
from post.services.post import PostService
from user.services.user import UserService


class PostAPITestCase(BaseUserTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def _create_post(
            self,
            title,
            content
    ):
        data = {
            'uts': get_uts(),
            'title': title,
            'content': content,
        }

        rsp = self.api_client.post(f'/api/post/', data=data)
        return PostService.filter(pk=rsp.json()['post_id']).first()

    def test_create_post(self):
        # ready
        title = 'title'
        content = 'content'
        data = {
            'uts': get_uts(),
            'title': title,
            'content': content,
        }

        # execute
        rsp = self.api_client.post(f'/api/post/', data=data)

        # assert
        self.assertEqual(rsp.status_code, 201)

        return_data = rsp.json()
        self.assertTrue('post_id' in return_data)
        self.assertTrue('title' in return_data)
        self.assertTrue('content' in return_data)
        self.assertTrue('author_id' in return_data)

    def test_get_post(self):
        post = self._create_post('title', 'content')

        # ready
        data = f'uts={get_uts()}'

        # execute
        rsp = self.api_client.get(f'/api/post/{post.id}/?{data}')

        # assert
        self.assertEqual(rsp.status_code, 200)

        return_data = rsp.json()
        self.assertTrue('post_id' in return_data)
        self.assertTrue('title' in return_data)
        self.assertTrue('content' in return_data)
        self.assertTrue('author_id' in return_data)

    def test_get_post_list(self):
        self._create_post('title1', 'content1')
        self._create_post('title2', 'content2')
        self._create_post('title3', 'content3')

        # ready
        data = f'uts={get_uts()}'

        # execute
        rsp = self.api_client.get(f'/api/post/?{data}')

        # assert
        self.assertEqual(rsp.status_code, 200)
