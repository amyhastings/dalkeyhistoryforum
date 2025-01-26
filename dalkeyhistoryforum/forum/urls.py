from django.urls import path
from .views import (
    TopicListView,
    ThreadListView,
    PostListView,
)
from . import views

urlpatterns = [
    path('', TopicListView.as_view(), name='forum-home'),
    path('threads_by_topic/<topic>', ThreadListView.as_view()),
    path('thread_post_list/<thread>', PostListView.as_view()),
    path('about/',views.about, name='forum-about'),
]