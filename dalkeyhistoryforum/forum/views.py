from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Thread, Post

def home(request):
    context = {
       'threads': Thread.objects.all()
    }
    return render(request, 'forum/home.html', context)

def about(request):
    return render(request, "forum/about.html", {"title": "About"})