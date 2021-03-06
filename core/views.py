from django.shortcuts import render
from django.http import HttpRequest

def index(request: HttpRequest):
    context = {
        "title": "A Discord User",
        "description": "I use Discord."
    }

    return render(request, "core/index.html", context)