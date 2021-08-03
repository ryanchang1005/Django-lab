from collections import namedtuple
from datetime import timedelta
from unittest.mock import patch
from freezegun import freeze_time

class EmailService:
    
    @staticmethod
    def send_by_static_method(text):
        print('send_by_static_method called')
    
    def send_by_instance_method(self, text):
        print('send_by_instance_method called')

class SMSService:
    def send_sms(self, text):
        print('send_sms')

def verify_something(secret_key, payload, signature):
    return False

class SampleTestCase(BaseAPITestCase):

    def test_add(self):
        self.assertEqual(1 + 1, 2)
    
    @patch.object(EmailService, 'send_by_static_method')
    def test_send_by_static_method(self, mock_send_by_static_method):
        def my_send(text):
            print('my_send called')
            return {}
        mock_send_by_static_method.side_effect = my_send
        mock_send_by_static_method.side_effect = lambda text: {}

        return_data = EmailService.send_by_static_method()
        self.assertEquals(return_data)
    
    @patch.object(EmailService, 'send_by_instance_method')
    def test_send_by_static_method(self, mock_send_by_instance_method):
        send_by_instance_method.side_effect = lambda text: {}

    @patch('my.module.verify')
    def test_mock_module_function(self, mock_verify):
        mock_verify.side_effect = lambda secret_key, payload, signature: True
        pass

    def test_call_api(self):
        data = {'title': 'xxx', 'content': 'xxx'}
        rsp = self.api_client.post('/api/posts/', data=data)
        return_data = rsp.json()

        # assert Response json data
        self.assertTrue('post_id' in return_data)
        self.assertTrue('title' in return_data)
        self.assertTrue('content' in return_data)
        self.assertEqual(return_data['title'], data['title'])
        self.assertEqual(return_data['content'], data['content'])
        
        # assert Model
        post = Post.objects.get(id=return_data['post_id'])
        self.assertIsNotNone(post)
        self.assertEqual(post.title, data['title'])
        self.assertEqual(post.content, data['content'])

    @patch.object(EmailService, 'send_by_instance_method')
    @patch.object(SMSService, 'send_sms')
    def test_mock_function_order(self, mock_send_sms, mock_send_by_instance_method):
        """
        參數順序左到右 對應@patch.object內到外
        """
        mock_send_sms.side_effect = lambda text: {}
        mock_send_by_instance_method.side_effect = lambda text: {}
    
    @patch.object(SMSService, 'send_sms')
    def test_mock_function_assert_call_with(self, mock_send_sms):
        mock_send_sms.side_effect = lambda text: {}

        text = 'xxx'
        SMSService.send_sms(text)

        mock_send_sms.assert_called_with(text)
        mock_send_sms.assert_called()

    def test_freezegun(self):
        now = get_now_datetime_obj()
        order = Order.objects.create(
            expire_time=now + timedelta(hours=1)
        )
        self.assertTrue(order.expire_time > now)

        with freeze_time(now + timedelta(hours=1, minutes=1)):
            self.assertTrue(order.expire_time < get_now_datetime_obj())