import os

from celery import Celery
from django.conf import settings

# 設置環境變量 DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 創建實例
app = Celery('core')
app.config_from_object('django.conf:settings')

# 查找在 INSTALLED_APPS 設置的異步任務
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# ================== 排程任務[Start] ==================
app.conf.beat_schedule = {
    # 'schedule_function': {
    #     'task': 'core.celery.schedule_function',
    #     'schedule': crontab(hour=12, minute=0),
    # },
}


@app.task(bind=True)
def schedule_function(self):
    pass


# ================== 排程任務[End] ==================

# ================== MessageQueue任務[Start] ==================
@app.task
def create_chat_message(chat_id, name, message, create_time):
    from chats.models import Chat
    from chats.models import ChatMessage

    chat = Chat.objects.get(pub_id=chat_id)

    chat_message = ChatMessage()
    chat_message.chat = chat
    chat_message.name = name
    chat_message.message = message
    chat_message.create_time = create_time
    chat_message.save()

# ================== MessageQueue任務[End] ==================
