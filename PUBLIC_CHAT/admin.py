from django.contrib import admin

# Register your models here.
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import PublicChatRoom,PublicChatRoomManager,PublicChatRoomMessage

"""     PUBLIC_CHAT_ROOM MODEL - ADMIN CLASS    """
class PublicChatRoomAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["id","title","user"]
    list_display = ["id","title"]

    class Meta:
        model = PublicChatRoom
# REGISTRATION OF PUBLIC_CHAT_ROOM
admin.site.register(PublicChatRoom, PublicChatRoomAdmin)


"""     CACHING_PAGINATOR   """
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


"""     PUBLIC_CHAT_ROOM_MESSAGE MODEL - ADMIN CLASS    """
class PublicChatRoomMessageAdmin(admin.ModelAdmin):
    list_display = ["room","user","timestamp"]
    list_filter = ["room","user","timestamp","content"]
    search_fields = ["room__title","user__username","content"]
    readonly_fields = ["id","user","room","timestamp"]

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = PublicChatRoomMessage
# REGISTRAION OF PUBLIC_CHAT_ROOM_MESSAGE
admin.site.register(PublicChatRoomMessage, PublicChatRoomMessageAdmin)