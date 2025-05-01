from django.db import models

from accounts.models import CustomUser

from django.conf import settings

from django.utils import timezone

# Create your models here.


class ChatRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_chats')
    counselor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='counselor_chats')
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'counselor')

    def __str__(self):
        return f"Chat {self.id}: {self.user} & {self.counselor}"
    
    

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"


