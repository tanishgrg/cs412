# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines the data models for the Mini Insta application.

from django.db import models


class Profile(models.Model):
    """Represents a user profile in the Mini Insta application."""

    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    bio_text = models.TextField()
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the username of this profile."""
        return self.username