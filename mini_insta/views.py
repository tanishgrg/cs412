# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines views for Mini Insta profiles and posts.

from django.views.generic import ListView, DetailView
from .models import Profile, Post


class ProfileListView(ListView):
    """Display a list of all Profile records."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display one Profile record and its posts."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display one Post record and its photos."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"
