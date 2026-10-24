# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines views for Mini Insta profiles and posts.

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import redirect
from .forms import CreateProfileForm
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import Follow, Like

class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    """Require login through the Mini Insta login page."""

    login_url = reverse_lazy("login")


class PostOwnerMixin(MiniInstaLoginRequiredMixin, UserPassesTestMixin):
    """Allow only the owner of a post to modify it."""

    def test_func(self):
        """Check whether the logged-in user owns the post."""
        post = self.get_object()
        return post.profile.user_id == self.request.user.pk

class ProfileListView(ListView):
    """Display a list of all profiles."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    """Display a profile and its posts."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """Add the logged-in user's profile and follow status."""
        context = super().get_context_data(**kwargs)

        context["viewer_profile"] = None
        context["is_following"] = False

        if self.request.user.is_authenticated:
            viewer = Profile.objects.filter(
                user=self.request.user
            ).first()

            context["viewer_profile"] = viewer

            if viewer:
                context["is_following"] = Follow.objects.filter(
                    profile=self.object,
                    follower_profile=viewer
                ).exists()

        return context


class MyProfileView(MiniInstaLoginRequiredMixin, DetailView):
    """Display the logged-in user's profile."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        """Return the profile belonging to the logged-in user."""
        return get_object_or_404(
            Profile,
            user=self.request.user
        )

class PostDetailView(DetailView):
    """Display a post, its photos, and the logged-in user's like status."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Add the viewer's profile and whether they liked the post."""
        context = super().get_context_data(**kwargs)

        context["viewer_profile"] = None
        context["has_liked"] = False

        if self.request.user.is_authenticated:
            viewer = Profile.objects.filter(
                user=self.request.user
            ).first()

            context["viewer_profile"] = viewer

            if viewer:
                context["has_liked"] = Like.objects.filter(
                    post=self.object,
                    profile=viewer
                ).exists()

        return context


class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    """Display and process the form for creating a new post."""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_profile(self):
        """Return the logged-in user's profile."""
        return get_object_or_404(
            Profile,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        """Add the logged-in user's profile to the template."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        return context

    def form_valid(self, form):
        """Save a post and its uploaded photos for the logged-in user."""
        form.instance.profile = self.get_profile()

        response = super().form_valid(form)

        files = self.request.FILES.getlist("files")

        for file in files:
            Photo.objects.create(
                post=self.object,
                image_file=file
            )

        return response

    def get_success_url(self):
        """Redirect to the newly created post."""
        return reverse("show_post", kwargs={"pk": self.object.pk})

class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    """Display and process the form for updating a profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def get_object(self, queryset=None):
        """Return the profile belonging to the logged-in user."""
        
        return get_object_or_404(Profile, user=self.request.user)

class UpdatePostView(PostOwnerMixin, UpdateView):
    """Display and process the form for updating a post."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self):
        """Redirect to the post detail page after updating."""
        return reverse("show_post", kwargs={"pk": self.object.pk})


class DeletePostView(PostOwnerMixin, DeleteView):
    """Display a confirmation form and delete a post."""

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the post and its profile to the template context."""
        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        """Redirect to the post owner's profile after deletion."""
        return reverse(
            "show_profile",
            kwargs={"pk": self.object.profile.pk}
        )

class ShowFollowersDetailView(DetailView):
    """Display the followers of a profile."""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Display the profiles followed by a profile."""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class ShowFeedView(MiniInstaLoginRequiredMixin, DetailView):
    """Display a feed of posts from profiles being followed."""

    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"
    def get_object(self, queryset=None):
        """Return the profile belonging to the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

class SearchView(MiniInstaLoginRequiredMixin, ListView):
    """Display a search form and matching profiles and posts."""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """Show the search form when no query has been submitted."""
        if "query" not in request.GET:
            profile = get_object_or_404(Profile, user=request.user)
            return render(
                request,
                "mini_insta/search.html",
                {"profile": profile}
            )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return posts with captions matching the query."""
        query = self.request.GET.get("query", "").strip()

        if not query:
            return Post.objects.none()

        return Post.objects.filter(
            caption__icontains=query
        ).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        """Add the current profile and matching search results."""
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "").strip()

        context["profile"] = get_object_or_404(
            Profile, user=self.request.user
        )
        context["query"] = query
        context["posts"] = context["object_list"]

        if query:
            context["profiles"] = Profile.objects.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query)
            )
        else:
            context["profiles"] = Profile.objects.none()

        return context


class CreateProfileView(CreateView):
    """Allow visitors to register and create a Mini Insta profile."""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add the Django user registration form to the context."""
        context = super().get_context_data(**kwargs)

        if "user_form" not in context:
            context["user_form"] = UserCreationForm()

        return context

    def post(self, request, *args, **kwargs):
        """Validate the user and profile forms together."""
        self.object = None

        profile_form = self.get_form()
        user_form = UserCreationForm(request.POST)

        profile_valid = profile_form.is_valid()
        user_valid = user_form.is_valid()

        if profile_valid and user_valid:
            with transaction.atomic():
                user = user_form.save()
                profile_form.instance.user = user
                self.object = profile_form.save()

            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )

            return redirect("my_profile")

        context = self.get_context_data(
            form=profile_form,
            user_form=user_form
        )
        return self.render_to_response(context)

class FollowProfileView(MiniInstaLoginRequiredMixin, View):
    """Allow the logged-in user to follow another profile."""

    def post(self, request, pk):
        """Create a follow relationship for the specified profile."""
        follower = get_object_or_404(Profile, user=request.user)
        profile = get_object_or_404(Profile, pk=pk)

        if follower == profile:
            return HttpResponseForbidden("You cannot follow yourself.")

        Follow.objects.get_or_create(
            profile=profile,
            follower_profile=follower
        )

        return redirect("show_profile", pk=pk)


class DeleteFollowView(MiniInstaLoginRequiredMixin, View):
    """Allow the logged-in user to unfollow another profile."""

    def post(self, request, pk):
        """Delete an existing follow relationship."""
        follower = get_object_or_404(Profile, user=request.user)
        profile = get_object_or_404(Profile, pk=pk)

        Follow.objects.filter(
            profile=profile,
            follower_profile=follower
        ).delete()

        return redirect("show_profile", pk=pk)


class LikePostView(MiniInstaLoginRequiredMixin, View):
    """Allow the logged-in user to like another user's post."""

    def post(self, request, pk):
        """Create a like for the specified post."""
        profile = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, pk=pk)

        if post.profile == profile:
            return HttpResponseForbidden("You cannot like your own post.")

        Like.objects.get_or_create(
            post=post,
            profile=profile
        )

        return redirect("show_post", pk=pk)


class DeleteLikeView(MiniInstaLoginRequiredMixin, View):
    """Allow the logged-in user to remove their like from a post."""

    def post(self, request, pk):
        """Delete the user's existing like."""
        profile = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, pk=pk)

        Like.objects.filter(
            post=post,
            profile=profile
        ).delete()

        return redirect("show_post", pk=pk)
