from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Topic, Thread, Post
from .forms import ThreadCreateForm, FirstPostCreateForm

User = get_user_model()

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

class PostListView(ListView):
    model = Post
    template_name = 'forum/thread_post_list.html'
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

class UserPostListView(ListView):
    model = Post
    template_name = 'forum/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-timestamp')
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['content']

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('view-thread', kwargs={'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['content']

    def get_context_data(self, *args, **kwargs):
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.thread = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse_lazy('view-thread', kwargs={'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        context['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        context['thread'] = get_object_or_404(Thread, id=self.kwargs['thread_id'])
        return context
            
    def get_success_url(self):
        return reverse_lazy('view-thread', kwargs={'topic_id': self.kwargs['topic_id'], 'thread_id': self.kwargs['thread_id']})

def about(request):
    return render(request, "forum/about.html", {"title": "About"})