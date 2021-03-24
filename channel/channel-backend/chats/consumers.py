import json

from channels.generic.websocket import AsyncWebsocketConsumer

from core.celery import create_chat_message

from core.utils.datetime import to_iso8601_utc_string, get_now_datetime_obj


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.chat_id = None

    async def connect(self):
        """
        WebSocket一連線進到的地方
        在此檢查
        """

        # Chat pub_id
        self.chat_id = self.scope["url_route"]["kwargs"]["pub_id"]

        # 加入
        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )

        # 連上
        await self.accept()

    async def disconnect(self, close_code):
        """
        斷開連線
        """

        # 離開群組
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        接收到client資料
        """
        data = json.loads(text_data)

        name = data['name']
        message = data['message']
        create_time = get_now_datetime_obj()

        create_chat_message.delay(self.chat_id, name, message, create_time)

        # 發送訊息
        await self.channel_layer.group_send(self.chat_id, {
            'type': 'chat_message',
            'name': name,
            'message': message,
            'create_time': to_iso8601_utc_string(create_time),
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'name': event['name'],
            'message': event['message'],
            'create_time': event['create_time'],
        }))
