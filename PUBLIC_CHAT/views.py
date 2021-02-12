from django.shortcuts import render

# Create your views here.
def public_chat(request):
    return render(request,"PUBLIC_CHAT/public_chat.html")

def room(request,room_name):
    return render(request,"PUBLIC_CHAT/public_chat_room.html",{
        "room_name":room_name
        })