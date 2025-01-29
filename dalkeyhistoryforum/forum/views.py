from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Topic, Thread, Post
from .forms import ThreadCreateForm, FirstPostCreateForm

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

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadListView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        return Thread.objects.filter(topic=self.topic).order_by('-timestamp')

class PostListView(ListView):
    model = Post
    template_name = 'forum/thread_post_list.html'
    fields = ['title', 'author', 'content', 'timestamp']
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return Post.objects.filter(thread=self.thread).order_by('timestamp')



@login_required
def create_thread(request):
    if request.method == 'POST':
        t_form = ThreadCreateForm(request.POST)
        p_form = FirstPostCreateForm(request.POST)

        if t_form.is_valid() and p_form.is_valid():
            thread = t_form.save(commit=False)
            thread.author = request.user
            thread.save()
            post = p_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect("/topic/%d/thread/%d" % (thread.topic.id, thread.id))

    else:
        t_form = ThreadCreateForm()
        p_form = FirstPostCreateForm()
    return render(request, 'forum/thread_form.html', {'t_form': t_form, 'p_form': p_form})


class CreatePostView(CreateView):
    model = Post
    fields = ['content']
    
    def form_valid(self, form):
        form.instance.thread_id = self.kwargs['pk']
        return super().form_valid(form)

def about(request):
    return render(request, "forum/about.html", {"title": "About"})