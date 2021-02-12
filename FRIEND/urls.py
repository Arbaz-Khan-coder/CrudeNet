from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('friend_list/<str:username>/',views.friends_list_view,name="CrudeNet-FriendList"),
    path('friend_remove/', views.remove_friend, name='CrudeNet-RemoveFriend'),
    path('friend_request/', views.send_friend_request, name='CrudeNet-FriendRequestSend'),
    path('friend_request_cancel/', views.cancel_friend_request, name='CrudeNet-FriendRequestCancel'),
    path('friend_requests/<user_id>/', views.friend_requests, name='CrudeNet-FriendRequest'),
    path('friend_request_accept/<friend_request_id>/', views.accept_friend_request, name='CrudeNet-FriendRequestAccept'),
    path('friend_request_decline/<friend_request_id>/', views.decline_friend_request, name='CrudeNet-FriendRequestDecline')
]