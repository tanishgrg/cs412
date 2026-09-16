from django.shortcuts import render 
 
import random
 
# Tanish Gurung
# tanishg@bu.edu
# CS412 Assignment 1
# Views for the Quote of the Day application with my GOAT Monkey D. Luffy.

# Create your views here.


def quote(request):
    """Display a randomly selected Luffy quote and image."""
    quotes = [
        "It’s not about whether I can or not. I’m gonna do it because I want to.",
        "It doesn’t matter if you’re a king or a god. It doesn’t matter who’s great or who’s not great!",
        "I have friends I want by my side, even if they’re not strong.",
        "I won’t go on a boring adventure!",
    ]
    images = [
        "https://www.belloflostsouls.net/wp-content/uploads/2023/09/luffy-anime.png",
        "https://static.wikia.nocookie.net/super-smash-keybladers/images/7/74/Monkey_D._Luffy_Anime_Pre_Timeskip_Full_Body.png/revision/latest?cb=20171211054404",
        "https://static0.srcdn.com/wordpress/wp-content/uploads/2025/05/one-piece-luffy-angry.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjClx0tujOHbAnbEGzMawJj7m-lV0EsquRqzYbixs1MlnBIBKbc42jY3M&s=10",
    ]

    index = random.randrange(len(quotes))

    context = {
        "quote": quotes[index],
        "image": images[index],
    }
    return render(request, "quotes/quote.html", context)

def show_all(request):

    """Display all Luffy quotes and images."""

    quotes = [
        "It’s not about whether I can or not. I’m gonna do it because I want to.",
        "It doesn’t matter if you’re a king or a god. It doesn’t matter who’s great or who’s not great!",
        "I have friends I want by my side, even if they’re not strong.",
        "I won’t go on a boring adventure!",
    ]

    images = [
        "https://www.belloflostsouls.net/wp-content/uploads/2023/09/luffy-anime.png",
        "https://static.wikia.nocookie.net/super-smash-keybladers/images/7/74/Monkey_D._Luffy_Anime_Pre_Timeskip_Full_Body.png/revision/latest?cb=20171211054404",
        "https://static0.srcdn.com/wordpress/wp-content/uploads/2025/05/one-piece-luffy-angry.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjClx0tujOHbAnbEGzMawJj7m-lV0EsquRqzYbixs1MlnBIBKbc42jY3M&s=10",
    ]

    context = {
        "quotes": quotes,
        "images": images,
    }

    return render(request, "quotes/show_all.html", context)


def about(request):
    """Display information about Luffy and the website creator."""
    return render(request, "quotes/about.html")