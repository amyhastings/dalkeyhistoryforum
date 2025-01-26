from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Topic, Thread, Post

# def home(request):
#     context = {
#        'topics': Topic.objects.all()
#     }
#     return render(request, 'forum/home.html', context)

class TopicListView(ListView):
    model = Topic
    template_name = 'forum/home.html'
    fields = ['title', 'description']
    context_object_name = 'topics'

class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'
    fields = ['title', 'author', 'timestamp']
    context_object_name = 'threads'
    paginate_by = 5

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, title=self.kwargs['topic'])
        return Thread.objects.filter(topic=self.topic).order_by('-timestamp')

class PostListView(ListView):
    model = Post
    template_name = 'forum/thread_post_list.html'
    fields = ['title', 'author', 'content', 'timestamp']
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, title=self.kwargs['thread'])
        return Post.objects.filter(thread=self.thread).order_by('timestamp')

class CreateThreadView(CreateView):
    model = Thread
    fields = ['title']
    success_url = reverse_lazy('thread_list')

class CreatePostView(CreateView):
    model = Post
    fields = ['content']
    
    def form_valid(self, form):
        form.instance.thread_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread_detail', kwargs={'pk': self.kwargs['pk']})

def about(request):
    return render(request, "forum/about.html", {"title": "About"})