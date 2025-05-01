import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protishruti.settings')
django.setup()

from accounts.models import CustomUser
from chat.models import ChatRoom, Message

# Create test users
user1 = CustomUser.objects.create_user(
    username='user1',
    password='testpass123',
    is_user=True
)
user2 = CustomUser.objects.create_user(
    username='counselor1',
    password='testpass123',
    is_counselor=True
)

# Create chat room
room = ChatRoom.objects.create(user=user1, counselor=user2)

# Create some messages
Message.objects.create(room=room, sender=user1, content="Hello counselor!")
Message.objects.create(room=room, sender=user2, content="Hi there! How can I help?")