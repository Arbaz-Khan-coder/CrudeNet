from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User

class PublicChatRoom(models.Model):
    title = models.CharField(max_length=80, unique=True, blank=False)
    users = models.ManyToManyField(User, blank=True, help_text="Users who are connected to the chat")

    def __str__(self):
        return f"PublicChat : {self.title}"

    def connect_user(self,user):
        """
        RETURN TRUE IF USER IS ADDED TO USERS LIST
        """
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added
    
    def disconnect_user(self,user):
        """
        RETURN TRUE IF USER IS REMOVED FROM USERS LIST
        """
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """
        RETURN THE CHANNELS GROUP NAME THAT SOCKETS SHOULD SUBSCRIBE TO AND GET SENT MESSAGES AS THEY ARE GENERATED
        """
        return f"PublicChatRoom - {self.id}"


class PublicChatRoomManager(models.Manager):
    def by_room(self,room):
        qs = PublicChatRoomMessage.objects.filter(room = room).order_by("_timestamp")
        return qs


class PublicChatRoomMessage(models.Model):
    """
    CHAT MESSAGS  CREATED BY A USER INSIDE A PUBLIC_CHAT_ROOM
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False,blank=False)

    object = PublicChatRoomManager()

    def __str__(self):
        return self.content