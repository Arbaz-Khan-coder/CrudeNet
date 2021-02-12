from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
from .forms import UserRegistrationForm,UserUpdateForm,UserDPForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from BLOG.models import Post,MediaPost_Write,MediaPost_Image,MediaPost_Video
from FRIEND.models import FriendList,FriendRequest
from FRIEND.friendRequest_status import FriendRequestStatus
from FRIEND.utils import get_friend_request_or_false
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json


@login_required
def profile_setting(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form =  UserDPForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f"Your Account has been updated")
            return redirect("CrudeNet-ProfileSetting")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserDPForm(instance=request.user.profile)
    content = {
        "p_form": p_form,
        "u_form": u_form,
    }
    return render(request, "LOGIN/profile_setting.html", content)


@login_required
def profile(request,**kwargs):
    payload = {}
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong")
    if account:
        num_post = 0
        num_blog = Post.objects.filter(author=account).count()
        num_post += MediaPost_Write.objects.filter(writer = account).count()
        num_post += MediaPost_Image.objects.filter(user = account).count()
        num_post += MediaPost_Video.objects.filter(user = account).count()
        posts = Post.objects.filter(author= account)
        username = account.username
        email = account.email
        dp_url = account.profile.dp.url
        acc_id = account.id
        user = request.user
        # FRIEND LIST
        try:
            friend_list = FriendList.objects.get(user = account) # THIS WILL GET FRIENDS LIST OF CURRENT LOGIN USER
        except FriendList.DoesNotExist:
            friend_list = FriendList(user = account) # IF FRIEND LIST DIDN'T EXIST IT WILL CREATE IT
            friend_list.save()
        friends = friend_list.friends.all() # THIS WILL GET FRIENDS
        content = {
            "posts":posts,
            "num_blog":num_blog,
            "num_post":num_post,
            "account":account,
            "username":username,
            "user":user,
            "id":acc_id,
            "email":email,
            "dp_url":dp_url,
            "friends":friends,

        }
        # DEFINE TEMPLATE VARIABLE
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SEND.value
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk = user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: REQUEST HAS BEEN SENT FROM THEM TO U: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SEND_TO_YOU.value
                    content["pending_friend_request_id"] = get_friend_request_or_false(sender=account, receiver=user).id

                # CASE2: REQUEST HAS BEEN SENT FROM U TO THEM: FRIENDREQUESTSTATUS.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SEND_TO_THEM.value 

                # CASE3: NO REQUEST HAS BEEN SENT: FRIENDREQUESTSTATUS.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SEND.value
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver = user, is_active = True)
            except:
                pass
        content["is_self"] = is_self
        content["is_friend"] = is_friend
        content["request_sent"] = request_sent
        content["friend_requests"] = friend_requests
        content["is_self"] = is_self
        return render(request,"LOGIN/profile.html",content)


@login_required
def blog_profile(request, **kwargs):
    posts_dic = {}
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong")
    if account:
        posts = Post.objects.filter(author= account)
        posts_dic["posts"] = posts
    return render(request,"LOGIN/blog_profile.html",posts_dic)


@login_required
def post_profile(request, **kwargs):
    posts_dic = {}
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong")
    if account:
        posts = MediaPost_Write.objects.filter(writer= account)
        posts_dic["posts"] = posts
        posts_dic["id"] = user_id
    return render(request,"LOGIN/post_profile.html",posts_dic)


@login_required
def image_profile(request, **kwargs):
    posts_dic = {}
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong")
    if account:
        posts = MediaPost_Image.objects.filter(user= account)
        posts_dic["posts"] = posts
        posts_dic["id"] = user_id
    return render(request,"LOGIN/image_profile.html",posts_dic)


@login_required
def video_profile(request, **kwargs):
    posts_dic = {}
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk = user_id)
    except:
        return HttpResponse("Something went wrong")
    if account:
        posts = MediaPost_Video.objects.filter(user= account)
        posts_dic["posts"] = posts
        posts_dic["id"] = user_id
    return render(request,"LOGIN/video_profile.html",posts_dic)


@csrf_exempt
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Account create for {username}.You can Login now")
            return redirect("CrudeNet-Login")
    else:
        form = UserRegistrationForm()
    return render(request,"LOGIN/register.html",{"form":form})


@login_required
def search(request):
    return render(request,"LOGIN/search.html")


