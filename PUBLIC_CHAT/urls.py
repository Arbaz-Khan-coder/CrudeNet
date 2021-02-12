from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('public_chat/',views.public_chat,name="CrudeNet-PublicChat"),
    path('<str:room_name>/',views.room,name="CrudeNet-PublicChatRoom"),
]