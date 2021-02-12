from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import Post,MediaPost_Write,MediaPost_Image,MediaPost_Video,PersonalTimeline,Comment
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from FRIEND.models import FriendList
from .filters import PostFilter
from LOGIN.forms import VideoForm,ImageForm,CommentForm
from django.forms import modelformset_factory


# NOTICE 
def notice(request):
    return render(request,"BLOG/notice.html")

# SEARCHING - FIILTER
def postsearch(request):
    blog = Post.objects.all()
    myfilter = PostFilter(request.GET, queryset=blog)
    search_blog = myfilter.qs
    return render(request,"BLOG/post_search.html",{'myfilter':myfilter,'search_blog':search_blog})


# SHOW YOUR FRIENDS TIMELINE
@login_required
def Media_TimelineList(request):
    current_user = request.user
    Friends_MediaStuff_LIST = []
    user = User.objects.get(username = current_user)
    try:
        friendlist = FriendList.objects.get(user = user)
    except FriendList.DoesNotExist:
        return HttpResponse(f"This User: {current_user} idoesn't have any friends")
    mine_Writestuff = MediaPost_Write.objects.filter(writer = user)
    for i in mine_Writestuff:
        Friends_MediaStuff_LIST.append(i)
    for friends in friendlist.friends.all():
        friend_WriteStuff = MediaPost_Write.objects.filter(writer = friends)
        for i in friend_WriteStuff:
            Friends_MediaStuff_LIST.append(i)
        Friends_MediaStuff_LIST.reverse()
    return render(request,"BLOG/timeline_home.html",{"media":Friends_MediaStuff_LIST})

# SHOW YOUR PERSONAL TIMELINE
@login_required
def Personal_TimelineList(request):
    current_user = request.user
    Timeline_list = []
    try:
        user = User.objects.get(username = current_user)
    except User.DoesNotExist:
        return HttpResponse(f"This User: {current_user} doesn't exist.")
    mine_timeline = PersonalTimeline.objects.filter(writer = user)
    for timelines in mine_timeline:
        Timeline_list.append(timelines)
    Timeline_list.reverse()
    return render(request,"BLOG/personal_timeline.html",{"media":Timeline_list})

# SHOW YOUR FRIENDS IMAGES
@login_required
def Media_ImageList(request):
    current_user = request.user
    Friends_MediaStuff_LIST = []
    user = User.objects.get(username = current_user)
    try:
        friendlist = FriendList.objects.get(user = user)
    except FriendList.DoesNotExist:
        return HttpResponse(f"This User: {current_user} is not in your Friend")
    mine_Writestuff = MediaPost_Image.objects.filter(user = user)
    for i in mine_Writestuff:
        Friends_MediaStuff_LIST.append(i)
    for friends in friendlist.friends.all():
        friend_WriteStuff = MediaPost_Image.objects.filter(user = friends)
        for i in friend_WriteStuff:
            Friends_MediaStuff_LIST.append(i)
    Friends_MediaStuff_LIST.reverse()
    return render(request,"BLOG/image_home.html",{"media":Friends_MediaStuff_LIST})


# SHOW YOUR FRIENDS VIDEOS
@login_required
def Media_VideoList(request):
    current_user = request.user
    Friends_MediaStuff_LIST = []
    user = User.objects.get(username = current_user)
    try:
        friendlist = FriendList.objects.get(user = user)
    except FriendList.DoesNotExist:
        return HttpResponse(f"This User: {current_user} is not in your Friend")
    mine_Writestuff = MediaPost_Video.objects.filter(user = user)
    for i in mine_Writestuff:
        Friends_MediaStuff_LIST.append(i)
    for friends in friendlist.friends.all():
        friend_WriteStuff = MediaPost_Video.objects.filter(user = friends)
        for i in friend_WriteStuff:
            Friends_MediaStuff_LIST.append(i)
    Friends_MediaStuff_LIST.reverse()
    return render(request,"BLOG/video_home.html",{"media":Friends_MediaStuff_LIST})


# UPLOAD IMAGE
@login_required
def ImageCreate(request):
    if request.method == "POST":
        i_form = ImageForm(request.POST, request.FILES)
        if i_form.is_valid():
            form = i_form.save(commit=False)
            form.user = request.user
            form.save()
            # messages.success(request, f"Your Account has been updated")
            return redirect("CrudeNet-ImageHome")
    else:
        i_form = ImageForm()
    content = {
        "i_form": i_form
    }
    return render(request, "BLOG/MediaPost_Image_form.html", content)


# UPLOAD VIDEO
@login_required
def VideoCreate(request):
    if request.method == "POST":
        v_form = VideoForm(request.POST, request.FILES)
        if v_form.is_valid():
            form = v_form.save(commit=False)
            form.user = request.user
            form.save()
            # messages.success(request, f"Your Account has been updated")
            return redirect("CrudeNet-VidoeHome")
    else:
        v_form = VideoForm()
    content = {
        "v_form": v_form
    }
    return render(request, "BLOG/MediaPost_Video_form.html", content)


# MEDIAPOST_WRITE - TIMELINE DETAIL
@login_required
def MediaPost_Write_detail(request,*args,**kwargs):
    post_id = kwargs.get("pk")
    content = {}
    post = MediaPost_Write.objects.get(id = post_id)
    post_comments = Comment.objects.filter(timeline = post.id)
    content["object"] = post
    content["comments_set"] = post_comments
    return render(request,"BLOG/MediaPost_Write_detail.html",content)


# SHOW BLOGS AT HOME PAGE
class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = "BLOG/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


# CREATE BLOG 
class PostCreateViews(LoginRequiredMixin,CreateView):
    model = Post
    fields = ["caption","content"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# CREATE WRITE POST
class WriteCreateViews(LoginRequiredMixin,CreateView):
    model = MediaPost_Write
    fields = ["content"]

    def form_valid(self,form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


# COMMENT TIMEINE
class CommentTimeline(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "BLOG/MediaPost_Write_Comment.html"

    def form_valid(self, form):
        form.instance.timeline_id = self.kwargs['pk']
        form.instance.commenter = self.request.user
        return super().form_valid(form)


# DELETE COMMENT 
class DeleteComment(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "BLOG/Comment_confirm_delete.html"
    success_url = "/home/timeline_home/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.commenter:
            return True
        else:
            return False

# CREATE PERSONAL TIMELINE
class PersonalTimelineViews(LoginRequiredMixin,CreateView):
    model = PersonalTimeline
    fields = ["content"]

    def form_valid(self,form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


# DETAIL BLOG
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = "BLOG/post_detail.html"


# DETAIL PERSONAL TIMELINE 
class PersonalTimelineDetailView(LoginRequiredMixin,DetailView):
    model = PersonalTimeline
    template_name = "BLOG/Personal_Timeline_detail.html"


# DELETE BLOG
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = "BLOG/post_confirm_delete.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


# DELETE WRITE POST
class WriteDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = MediaPost_Write
    template_name = "BLOG/MediaPost_Write_confirm_delete.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.writer:
            return True
        else:
            return False


# DELETE PERSONAL TIMELINE
class Personal_Timeline_DeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = PersonalTimeline
    template_name = "BLOG/Personal_Timeline_confirm_delete.html"
    success_url = "/home/personal_timeline"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.writer:
            return True
        else:
            return False

# DELETE IMAGE POST
class ImageDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = MediaPost_Image
    template_name = "BLOG/MediaPost_Image_confirm_delete.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

# DELETE IMAGE POST
class VideoDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = MediaPost_Video
    template_name = "BLOG/MediaPost_Video_confirm_delete.html"
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False


# EDIT BLOG
class PostEditViews(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ["caption","content"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


# EDIT WRITE POST
class WriteEditViews(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = MediaPost_Write
    fields = ["content"]

    def form_valid(self,form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.writer:
            return True
        else:
            return False


# EDIT PERSONAL TIMELINE
class Personal_Timeline_EditViews(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = PersonalTimeline
    fields = ["content"]

    def form_valid(self,form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.writer:
            return True
        else:
            return False

# SHOW SEARCH RESULT
def search_result(request,*args,**kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("search_box")
        if len(search_query) >0:
            search_results = User.objects.filter(username__icontains=search_query)
            current_user = request.user
            accounts = []
            for account in search_results:
                accounts.append((account,False))
            context['accounts'] = accounts

    return render(request,"BLOG/search_result.html",context)   



# UPLOAD IMAGE 
# @login_required
# def ImageCreate(request):
#     ImageFormSet = modelformset_factory(MediaPost_Image, form=ImageForm, extra = 5)
#     if request.method == "POST":
#         caption_form = CaptionOfImage(request.POST)
#         formset = ImageFormSet(request.POST, request.FILES, queryset = MediaPost_Image.objects.none())
#         if formset.is_valid() and caption_form.is_valid():
#             caption = caption_form.save(commit=False)
#             caption.user = request.user
#             caption.save()

#             for form in formset.cleaned_data:
#                 if form:
#                     image = form["image"]
#                     photo = MediaPost_Image(caption = caption,image = image)
#                     photo.save()
#             return HttpResponse(caption.errors, formset.errors)

#         # i_form = ImageForm(request.POST, request.FILES)
#         # if i_form.is_valid():
#         #     form = i_form.save(commit=False)
#         #     form.user = request.user
#         #     form.save()
#         #     return redirect("CrudeNet-ImageHome")
#     else:
#         c_form = CaptionOfImage()
#         i_form = ImageFormSet(queryset = MediaPost_Image.objects.none())
#     content = {
#         "c_form":c_form,
#         "i_form": i_form
#     }
#     return render(request,"BLOG/MediaPost_Image_form.html",content)

# @login_required
# def ImageCreate(request):
#     if request.method == "POST":
#         form  = ImageForm(request.POST ,request.FILES)
#         files = request.FILES.getlist("images")
#         print("before")
#         if form.is_valid():
#             print("before1")
#             user = request.user
#             title = form.cleaned_data['caption']
#             note_obj = ImageCaption.objects.create(user = user,caption = title)
#             for f in files:
#                 MediaPost_Image.objects.create(caption = note_obj,image = f)
#         else:
#             return HttpResponse("form invalid")
#     else:
#         c_form = ImageForm()
#         return render(request,"BLOG/MediaPost_Image_form.html",{"c_form":c_form})
