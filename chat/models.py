from django.db import models


class User(models.Model):
    name = models.CharField(max_length=45)
    blocked_users = models.ForeignKey("self", on_delete=models.CASCADE)


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=32, unique=True)


class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.OneToOneField(ChatRoom, on_delete=models.CASCADE)