from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # NOTICE URL
    path('notice',views.notice,name="CrudeNet-Notice"),
    # HOME URL
    path('home/',views.PostListView.as_view(),name="CrudeNet-Home"),
    path('home/timeline_home/',views.Media_TimelineList,name="CrudeNet-TimeLineHome"),
    path('home/image_home/',views.Media_ImageList,name="CrudeNet-ImageHome"),
    path('home/vidoe_home/',views.Media_VideoList,name="CrudeNet-VidoeHome"),
    #  BLOG URLS
    path('post/create/',views.PostCreateViews.as_view(),name="CrudeNet-AddPost"),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name="CrudeNet-DetailPost"),
    path('post/<int:pk>/delete',views.PostDeleteView.as_view(),name="CrudeNet-DeletePost"),
    path('post/<int:pk>/edit',views.PostEditViews.as_view(),name="CrudeNet-EditPost"),
    # POST - WRITE URLS
    path('post/write/create/',views.WriteCreateViews.as_view(),name="CrudeNet-AddWritePost"),
    path('post/write/<int:pk>/',views.MediaPost_Write_detail,name="CrudeNet-WriteDetailPost"),
    path('post/write/<int:pk>/comment/',views.CommentTimeline.as_view(),name="CrudeNet-WriteCommentPost"),
    path('post/write/comment/<int:pk>/delete',views.DeleteComment.as_view(),name="CrudeNet-DeleteComment"),
    path('post/write/<int:pk>/delete',views.WriteDeleteView.as_view(),name="CrudeNet-WriteDeletePost"),
    path('post/write/<int:pk>/edit',views.WriteEditViews.as_view(),name="CrudeNet-WriteEditPost"),
    # POST - IMAGE URLS
    path('post/image/create/',views.ImageCreate,name="CrudeNet-AddImagePost"),
    path('post/image/<int:pk>/delete',views.ImageDeleteView.as_view(),name="CrudeNet-ImageDeletePost"),
    # POST - VIDEO URLS
    path('post/video/create',views.VideoCreate,name="CrudeNet-AddVideoPost"),
    path('post/vidoe/<int:pk>/delte',views.VideoDeleteView.as_view(),name="CrudeNet-VideoDeletePost"),
    # PERSONAL TIMELINE URLS
    path('home/personal_timeline/',views.Personal_TimelineList,name="CrudeNet-PersonalTimeLine"),
    path('post/personal_timeline/create/',views.PersonalTimelineViews.as_view(),name="CrudeNet-AddPersonalTiimeline"),
    path('post/personal_timeline/<int:pk>/',views.PersonalTimelineDetailView.as_view(),name="CrudeNet-PersonalTimelineDetail"),
    path('post/personal_timeline/<int:pk>/delete',views.Personal_Timeline_DeleteView.as_view(),name="CrudeNet-PersonalTimelineDelete"),
    path('post/personal_timeline/<int:pk>/edit',views.Personal_Timeline_EditViews.as_view(),name="CrudeNet-PersonalTimelineEdit"),
    # SEARCH URL
    path("search_result/",views.search_result,name = "CrudeNet-SearchResult"),
    path('post/search/',views.postsearch,name="CrudeNet-SearchPost"),
]