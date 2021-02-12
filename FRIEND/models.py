from django.db import models

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
"""     FRIEND LIST MODEL    """
class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="User")
    friends = models.ManyToManyField(User, blank=True, related_name="Friends")

    def __str__(self):
        return f"{self.user.username} FriendList"

    def add_friend(self,account):
        # ADD NEW FRIEND
        if not account in self.friends.all(): #this wil check if that account i already a friend with user account
            self.friends.add(account)# ths will add friend account in friend list
            self.save()

    def remove_friend(self,account):
        # REMOVE FRIEND
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self,remove):
        # INITIATE THE ACTION OF UNFRIENDING SOMEONE
        remover_friend_list = self #PERSON DESTROYING THE FRIENDSHIP

        # REMOVE FRIEND FROM REMOVER FRIEND LIST
        remover_friend_list.remove_friend(remove)

        # REMOVE FRIEND FROM RMEOVE FRIEND LIST
        friend_list = FriendList.objects.get(user = remove)
        friend_list.remove_friend(remover_friend_list.user)

    def is_mutual_friend(self,friend):
        # IS THIS A FRIEND?
        if friend in self.friends.all():
            return True
        return False



"""     FRIEND REQUEST MODEL    """
class FriendRequest(models.Model):
    """
    A FRIEND REQUEST MODEL CONSISTS OF TWO MAIN PARTS:
        1.SENDER - person sending friend request
        2.RECEIVER - person receiving friend request
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver")
    
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        ACCEPT A FRIEND REQEUST
        UPDATE  BOTH SENDER & RECEIVER  FRIEND LIST
        """

        receiver_friend_list = FriendList.objects.get(user = self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user = self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        DECLINE A FRIEND REQUEST
        IT IS 'DECLINE' BY SETTING THE 'IS_ACTIVE' TO FALSE
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        CANCEL A FRIEND REQUEST
        IT IS 'CANCELLED'  BY SETTING THE 'IS_ACTIVE' TO FALSE
        THIS IS ONLY DIFFERENT  WITH 'DECLINING' THROUGH  THE NOTIFICATION THAT IS GENERATED
        """
        self.is_active = False
        self.save()