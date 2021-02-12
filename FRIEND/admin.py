from django.contrib import admin

from .models import FriendList,FriendRequest
# Register your models here.

"""     FRIENDLIST MODEL - ADMIN CLASS    """
class FriendListAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    list_display = ["user"]
    search_fields = ["user"]
    readonly_fields = ["user"]

    class Meta:
        model = FriendList
# REGISTRATION OF FRIENDLIST MODEL
admin.site.register(FriendList, FriendListAdmin)


"""     FRIENDREQUEST MODEL - ADMIN CLASS    """
class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ["sender","receiver"]
    list_display = ["sender","receiver"]
    search_fields = ["sender__username","sender__email","receiver__username","receiver__email"]

    class Meta:
        model = FriendRequest
# REGISTRAION OF FRIENDREQUEST MODEL
admin.site.register(FriendRequest, FriendRequestAdmin)