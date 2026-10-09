# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines views for Mini Insta profiles and posts.

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Profile, Post, Photo
from .forms import CreatePostForm


class ProfileListView(ListView):
    """Display a list of all profiles."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display one profile and its posts."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display one post and its photos."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    """Display and process the form for creating a new post."""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the profile from the URL to the template context."""
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        context["profile"] = profile
        return context


    def form_valid(self, form):
        """Save the new post and its uploaded photo files."""
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        form.instance.profile = profile

        response = super().form_valid(form)

        # Previously, photos were created from image URLs.
        # image_url = form.cleaned_data.get("image_url")

        files = self.request.FILES.getlist("files")

        for file in files:
            Photo.objects.create(
                post=self.object,
                image_file=file
            )

        return response

    

    def get_success_url(self):
        """Return the detail page URL for the newly created post."""
        return reverse("show_post", kwargs={"pk": self.object.pk})
