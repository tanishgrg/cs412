# Author: Tanish Gurung (tanishg@bu.edu)
# Description: Registers Mini Insta models with the Django admin site.

from django.contrib import admin
from .models import Profile


admin.site.register(Profile)