# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Registers Mini Insta models with the Django admin.

from django.contrib import admin
from .models import Profile, Post, Photo

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
