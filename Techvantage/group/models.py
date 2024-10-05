from django.db import models
from authapp.models import FirebaseUser

def get_default_user():
    user, created = FirebaseUser.objects.get_or_create(
        uid='Default_uid', 
        defaults={'email': 'default@example.com', 'display_name': 'Default User'}
    )
    return user.id  # Return the ID of the user

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Membership(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='memberships')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)  # Track when the user joined the room

    class Meta:
        unique_together = ('user', 'chat_room')  # Prevent the same user from joining a room multiple times

    def __str__(self):
        return f'{self.user.email} joined {self.chat_room.name}'

    
class Message(models.Model):
    content = models.TextField(blank=False)
    date_published = models.DateTimeField(auto_now_add=True)
    sender  = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='messages', default=get_default_user)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.user.username} in {self.chat_room.name}: {self.content[:20]}...'