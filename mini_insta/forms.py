# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines forms for creating Mini Insta posts.

from django import forms
from .models import Post, Profile


class CreatePostForm(forms.ModelForm):
    """Form for creating a new post."""

    class Meta:
        """Configure the model and fields used by the form."""

        model = Post
        fields = ["caption"]

class UpdateProfileForm(forms.ModelForm):
    """Form for updating an existing profile."""

    class Meta:
        """Configure which profile fields can be updated."""

        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]


class UpdatePostForm(forms.ModelForm):
    """Form for updating the caption of an existing post."""

    class Meta:
        """Configure the model and editable fields."""

        model = Post
        fields = ["caption"]

class CreateProfileForm(forms.ModelForm):
    """Form for creating a new Mini Insta profile."""

    class Meta:
        """Define the fields for creating a profile."""

        model = Profile
        fields = [
            "username",
            "display_name",
            "profile_image_url",
            "bio_text"
        ]