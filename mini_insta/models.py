# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Defines the data models for the Mini Insta application.

from django.db import models
from django.urls import reverse


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

    def get_all_posts(self):
        """Return all posts belonging to this profile, newest first."""
        return Post.objects.filter(profile=self).order_by("-timestamp")
        
    def get_absolute_url(self):
        """Return the URL of this profile's detail page."""
        return reverse("show_profile", kwargs={"pk": self.pk})
    def get_followers(self):
        """Return a list of profiles following this profile."""
        follows = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in follows]

    def get_num_followers(self):
        """Return the number of followers this profile has."""
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of profiles this profile follows."""
        follows = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in follows]

    def get_num_following(self):
        """Return the number of profiles this profile follows."""
        return Follow.objects.filter(follower_profile=self).count()
    def get_post_feed(self):
        """Return posts from followed profiles, newest first."""
        following = self.get_following()

        return Post.objects.filter(
            profile__in=following
        ).order_by("-timestamp")


class Post(models.Model):
    """Represents an Instagram post created by a profile."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return a string representation of this post."""
        return f"Post {self.pk} by {self.profile.username}"

    def get_all_photos(self):
        """Return all photos associated with this post."""
        return Photo.objects.filter(post=self).order_by("timestamp")
    def get_all_comments(self):
        """Return all comments on this post, oldest first."""
        return Comment.objects.filter(post=self).order_by("timestamp")

    def get_likes(self):
        """Return all likes associated with this post."""
        return Like.objects.filter(post=self)



class Photo(models.Model):
    """Represents a photo associated with a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="mini_insta/", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        """Return the uploaded image URL or the original image URL."""
        if self.image_file:
            return self.image_file.url
        return self.image_url

    def __str__(self):
        """Return a string representation of this photo."""
        if self.image_file:
            return f"Uploaded photo {self.pk} for Post {self.post.pk}"
        return f"URL photo {self.pk} for Post {self.post.pk}"

class Follow(models.Model):
    """Represents one profile following another profile."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    follower_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="follower_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a description of the follow relationship."""
        return f"{self.follower_profile.username} follows {self.profile.username}"


class Comment(models.Model):
    """Represents a comment made by a profile on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        """Return a description of this comment."""
        return f"{self.profile.username}: {self.text}"


class Like(models.Model):
    """Represents a profile liking a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a description of this like."""
        return f"{self.profile.username} likes Post {self.post.pk}"