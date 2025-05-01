from django.db import models

from django.conf import settings

from django.utils import timezone

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    counselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='counselor_chatrooms')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_chatrooms')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat between {self.counselor.username} and {self.user.username}"
    
    class Meta:
        unique_together = ('counselor', 'user')
        
        
    
    
    
    class Message(models.Model):
        chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
        sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='sent_messages')
        content = models.TextField()
        timestamp = models.DateTimeField(default=timezone.now)
        
        is_read=models.BooleanField(default=False)
        
        
        
        def __str__(self):
            return f"Message from {self.sender.username} at{self.timestamp}"
        
        class Meta:
            ordering = ['timestamp']