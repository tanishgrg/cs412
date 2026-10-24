# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines URL patterns for Mini Insta.

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    ProfileListView,
    ProfileDetailView,
    PostDetailView,
    CreatePostView,
    UpdateProfileView,
    UpdatePostView,
    DeletePostView,
    ShowFollowersDetailView,
    ShowFollowingDetailView,
    ShowFeedView,
    SearchView,
    MyProfileView,
    CreateProfileView,
    FollowProfileView,
    DeleteFollowView,
    LikePostView,
    DeleteLikeView,
)

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("create_profile", CreateProfileView.as_view(), name="create_profile"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),

    # Logged-in user's profile
    path("profile", MyProfileView.as_view(), name="my_profile"),
    # Create and update
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),

    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),

    # Followers and following
    path(
        "profile/<int:pk>/followers",
        ShowFollowersDetailView.as_view(),
        name="show_followers"
    ),

    path(
        "profile/<int:pk>/following",
        ShowFollowingDetailView.as_view(),
        name="show_following"
    ),

    # Feed and search
    path("profile/feed", ShowFeedView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),

    # Authentication
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="mini_insta/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="show_all_profiles"
        ),
        name="logout"
    ),
    # Following and unfollowing profiles
    path(
        "profile/<int:pk>/follow",
        FollowProfileView.as_view(),
        name="follow_profile"
    ),

    path(
        "profile/<int:pk>/delete_follow",
        DeleteFollowView.as_view(),
        name="delete_follow"
    ),

    # Liking and unliking posts
    path(
        "post/<int:pk>/like",
        LikePostView.as_view(),
        name="like_post"
    ),

    path(
        "post/<int:pk>/delete_like",
        DeleteLikeView.as_view(),
        name="delete_like"
    ),
]
