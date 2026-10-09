# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines forms for creating Mini Insta posts.

from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    """Form for creating a new post."""

    image_url = forms.URLField(required=False)

    class Meta:
        """Configure the model and fields used by the form."""

        model = Post
        fields = ["caption"]
