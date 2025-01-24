from django.contrib import admin
from .models import Topic, Thread, Post

admin.site.register(Topic, Thread, Post)
