"""
File: urls.py
Name: Tanish Gurung
BU Email: tanishg@bu.edu

Description:
Defines the URL routes for the restaurant application.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.main, name="main"),
    path("order/", views.order, name="order"),
    path("confirmation/", views.confirmation, name="confirmation"),
]