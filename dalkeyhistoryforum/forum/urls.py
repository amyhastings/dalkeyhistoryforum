from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    TopicListView,
    ThreadListView,
    PostListView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views
from forum import views as forum_views

urlpatterns = [
    path('', TopicListView.as_view(), name='forum-home'),
    path('topic/<int:topic_id>', ThreadListView.as_view(), name='threads-by-topic'),
    path('thread/new/', forum_views.create_thread, name='thread-create'),
    path('topic/<int:topic_id>/thread/<int:thread_id>', PostListView.as_view(), name='view-thread'),
    path('topic/<int:topic_id>/thread/<int:thread_id>/post/new', forum_views.create_comment, name='post-create'),
    path('topic/<int:topic_id>/thread/<int:thread_id>/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('topic/<int:topic_id>/thread/<int:thread_id>/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/',views.about, name='forum-about'),
    path('error/',views.error, name='forum-error'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)