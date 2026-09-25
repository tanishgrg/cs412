"""
File: views.py
Name: Tanish Gurung
BU Email: tanishg@bu.edu

Description:
Contains the view functions for the restaurant application, including
the main page, order page, and order confirmation page.
"""


from django.shortcuts import render
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def main(request):
    """Display the restaurant main page."""
    return render(request, "restaurant/main.html")


def order(request):
    """Display the order form with a randomly selected daily special."""

    specials = [
        "Spicy Chicken Sandwich",
        "Steak Tacos",
        "BBQ Burger",
        "Chicken Alfredo",
    ]

    daily_special = random.choice(specials)

    context = {
        "daily_special": daily_special,
    }

    return render(request, "restaurant/order.html", context)


def confirmation(request):
    """Process an order and display the confirmation page."""

    items = []
    total = 0

    if request.POST.get("burger"):
        items.append("Burger")
        total += 10

    if request.POST.get("fries"):
        items.append("Fries")
        total += 5

    if request.POST.get("pizza"):
        items.append("Pizza")
        total += 12

    if request.POST.get("special"):
        special = request.POST.get("special")
        items.append(special)
        total += 15

    if request.POST.get("pepperoni"):
        items.append("Pepperoni")
        total += 2

    if request.POST.get("mushrooms"):
        items.append("Mushrooms")
        total += 1

    name = request.POST.get("name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    instructions = request.POST.get("instructions")

    minutes = random.randint(30, 60)

    now = datetime.now(ZoneInfo("America/New_York"))
    ready_time = now + timedelta(minutes=minutes)
    ready_time = ready_time.strftime("%I:%M %p")

    context = {
        "items": items,
        "total": total,
        "name": name,
        "phone": phone,
        "email": email,
        "instructions": instructions,
        "ready_time": ready_time,
    }

    return render(request, "restaurant/confirmation.html", context)