from django.contrib import admin


# Register your models here.
from .models import Post,MediaPost_Write,MediaPost_Video,MediaPost_Image,PersonalTimeline,Comment

"""     POST MODEL - ADMIN CLASS    """
class PostAdmin(admin.ModelAdmin):
    list_filter = ["author","caption"]
    list_display = ["author"]
    search_fields = ["author","caption","date_posted"]
    readonly_fields = ["author","caption"]
    
    class Meta:
        model = Post
# REGISTRATION OF POST MODEL
admin.site.register(Post, PostAdmin)


"""     MEDIAPOST_WRITE - ADMIN CLASS   """
class MediaPost_WriteAdmin(admin.ModelAdmin):
    list_filter = ["writer"]
    list_display = ["writer"]
    search_fields = ["writer","date_posted"]
    readonly_fields = ["writer"]
    
    class Meta:
        model = MediaPost_Write
# REGISTRATION OF MEDIAPOST_WRITE MODEL
admin.site.register(MediaPost_Write, MediaPost_WriteAdmin)


"""     COMMENT TIMELINE - ADMIN CLASS   """
class Comment_TimelineAdmin(admin.ModelAdmin):
    list_filter = ["commenter","timeline","date_added"]
    list_display = ["commenter"]
    search_fields = ["commenter","timeline","date_added"]
    readonly_fields = ["commenter"]
    
    class Meta:
        model = Comment
# REGISTRATION OF MEDIAPOST_WRITE MODEL
admin.site.register(Comment, Comment_TimelineAdmin)


"""     MEDIAPOST_IMAGE - ADMIN CLASS   """
class MediaPost_ImageAdmin(admin.ModelAdmin):
    list_filter = ["user","caption"]
    list_display = ["user"]
    search_fields = ["user","caption","date_posted"]
    readonly_fields = ["user"]
    
    class Meta:
        model = MediaPost_Image
# REGISTRATION OF MEDIAPOST_IMAGAE MODEL
admin.site.register(MediaPost_Image, MediaPost_ImageAdmin)


"""     MEDIAPOST_VIDEO - ADMIN CLASS   """
class MediaPost_VideoAdmin(admin.ModelAdmin):
    list_filter = ["user","caption"]
    list_display = ["user"]
    search_fields = ["user","caption","date_posted"]
    readonly_fields = ["user"]
    
    class Meta:
        model = MediaPost_Video
# REGISTRATION OF MEDIAPOST_IMAGAE MODEL
admin.site.register(MediaPost_Video, MediaPost_VideoAdmin)


"""     PERSONALTIMELINE - ADMIN CLASS   """
class PersonalTimeline_Admin(admin.ModelAdmin):
    list_filter = ["writer"]
    list_display = ["writer"]
    search_fields = ["writer","date_posted"]
    readonly_fields = ["writer"]
    
    class Meta:
        model = PersonalTimeline
# REGISTRATION OF PERSONALTIMELINE MODEL
admin.site.register(PersonalTimeline, PersonalTimeline_Admin)