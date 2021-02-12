from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name="CrudeNet-Register"),
    path('login/',auth_views.LoginView.as_view(template_name = "LOGIN/login.html"),name="CrudeNet-Login"),
    path('logout/',auth_views.LogoutView.as_view(template_name = "LOGIN/logout.html"),name="CrudeNet-Logout"),
    path("profile/<int:user_id>/",views.profile,name = "CrudeNet-Profile"),
    path("profile/blog/<int:user_id>/",views.blog_profile,name = "CrudeNet-BlogProfile"),
    path("profile/post/timeline/<int:user_id>/",views.post_profile,name = "CrudeNet-PostProfile"),
    path("profile/post/image/<int:user_id>/",views.image_profile,name = "CrudeNet-ImageProfile"),
    path("profile/post/video/<int:user_id>/",views.video_profile,name = "CrudeNet-VideoProfile"),
    path("profile_setting/",views.profile_setting,name = "CrudeNet-ProfileSetting"),
    path("search/",views.search,name = "CrudeNet-Search"),
    
]