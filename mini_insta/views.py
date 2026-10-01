# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines the views for displaying Mini Insta profiles.

from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    """Display a list of all Profile records."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display one Profile record."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"