from django.urls import path
from .views import (
    TopicListView,
    ThreadListView,
    PostListView,
    PostCreateView,
)
from . import views
from forum import views as forum_views

urlpatterns = [
    path('', TopicListView.as_view(), name='forum-home'),
    path('topic/<int:topic_id>', ThreadListView.as_view(), name='threads-by-topic'),
    path('thread/new/', forum_views.create_thread, name='create-thread'),
    path('topic/<int:topic_id>/thread/<int:thread_id>', PostListView.as_view(), name='view-thread'),
    path('topic/<int:topic_id>/thread/<int:thread_id>/post/new', PostCreateView.as_view(), name='post-create'),
    path('about/',views.about, name='forum-about'),
]