from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from .formatchecker import ContentTypeRestrictedFileField
from django.template.defaultfilters import slugify


class Post(models.Model):
    caption = models.CharField(max_length=60,default="")
    date_posted = models.DateField(default = timezone.now)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete = models.CASCADE)


    def __str__(self):
        return f"{self.author}_{self.caption}"


    def get_absolute_url(self):
        return reverse("CrudeNet-Home")

class PersonalTimeline(models.Model):
    writer = models.ForeignKey(User,on_delete = models.CASCADE)
    date_posted = models.DateField(default = timezone.now)
    content = models.TextField()


    def __str__(self):
        return f"{self.writer.username}"


    def get_absolute_url(self):
        return reverse("CrudeNet-PersonalTimeLine")

class MediaPost_Write(models.Model):
    writer = models.ForeignKey(User,on_delete = models.CASCADE)
    date_posted = models.DateField(default = timezone.now)
    content = models.TextField()


    def __str__(self):
        return self.writer.username


    def get_absolute_url(self):
        return reverse("CrudeNet-TimeLineHome")
        
class Comment(models.Model): 
    timeline = models.ForeignKey(MediaPost_Write, on_delete = models.CASCADE, related_name ='comments') 
    commenter = models.ForeignKey(User, on_delete = models.CASCADE) 
    comments = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{str(self.commenter.username)} Comments | {str(self.date_added)}"

    def get_absolute_url(self):
        return reverse("CrudeNet-TimeLineHome")

class MediaPost_Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.CharField(max_length=48,default = "",)
    image = models.ImageField(upload_to="post_pics")
    date_posted = models.DateField(default = timezone.now)


    def __str__(self):
        return f"{self.user.username} Image"
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height>1000 or img.width>1000:
            img.thumbnail((400,400))
            img.save(self.image.path)

class MediaPost_Video(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    caption = models.CharField(max_length=44,default="")
    date_posted = models.DateField(default = timezone.now)
    # video = models.FileField(upload_to="post_video",null=True,verbose_name="",max_length="20971520")
    video = ContentTypeRestrictedFileField(upload_to='post_video', content_types=['video/mp4'],max_upload_size=10485760,blank=True, null=True)
    


    def __str__(self):
        return f"{self.user.username}_{self.video} Video"


    def get_absolute_url(self):
        return reverse("CrudeNet-Home")

# class MediaPost_ImageVide(models.Model):
#     user = models.ForeignKey(User,on_delete = models.CASCADE)
#     caption = models.CharField(max_length=80,default="")
#     date_posted = models.DateField(default = timezone.now)
#     data = models.content

# ContentTypeRestrictedFileField(upload_to='uploads/', content_types=['video/x-msvideo', 'application/pdf', 'video/mp4', 'audio/mpeg', ],max_upload_size=5242880,blank=True, null=True)

# class ImageCaption(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # date_posted = models.DateField(default = timezone.now)
    # caption = models.CharField(max_length=80,default="")