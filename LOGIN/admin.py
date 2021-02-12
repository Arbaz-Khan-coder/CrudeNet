from django.contrib import admin

# Register your models here.
from .models import Profile
from django.contrib.auth.models import User

"""     PROFILE MODEL - ADMIN CLASS     """
class ProfileAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    list_display = ["user"]
    search_fields = ["user"]
    readonly_fields = ["user"]

    class Meta:
        model = Profile
# REGISTRATION OF PROFILE MODEL
admin.site.register(Profile,ProfileAdmin)

