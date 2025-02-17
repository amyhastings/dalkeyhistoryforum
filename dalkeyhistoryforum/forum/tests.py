from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Topic, Thread, Post
from .forms import CommentCreateForm

class ThreadModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.topic = Topic.objects.create(title='Test Topic')
        cls.thread = Thread.objects.create(
            author=cls.user,
            topic=cls.topic,
            title='Test Thread',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            thread=cls.thread,
            content='This is a test first post on a thread'
        )

    def test_thread_str_method(self):
        thread = Thread.objects.get(id=1)
        self.assertEqual(str(thread), thread.title)

    def test_get_absolute_url(self):
        thread = Thread.objects.get(id=1)
        self.assertEqual(thread.get_absolute_url(), reverse('view-thread', kwargs={"topic_id": self.topic.id, "thread_id": self.thread.id}))

class ThreadViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.topic = Topic.objects.create(title='Test Topic')
        self.thread = Thread.objects.create(
            author=self.user,
            topic=self.topic,
            title='Test Thread',
        )
    
    def test_thread_list_view(self):
        url = reverse('threads-by-topic', kwargs={"topic_id": self.topic.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Thread')
        self.assertTemplateUsed(response, 'forum/thread_list.html')

    def test_create_thread_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('thread-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/thread_form.html')

        response = self.client.post(reverse('thread-create'), {
            'title': 'New title',
            'topic': '1',
            'content': 'New first post',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Thread.objects.filter(title='New title').exists())

class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.thread_user = User.objects.create_user(username='threaduser', password='54321')
        cls.topic = Topic.objects.create(title='Test Topic')
        cls.thread = Thread.objects.create(title='Test Thread', author=cls.thread_user, topic=cls.topic)
        cls.post = Post.objects.create(
            author=cls.user,
            thread=cls.thread,
            content='This is a test post'
        )

    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_author = f'{post.author}'
        expected_thread = f'{post.thread}'
        expected_content = f'{post.content}'
        self.assertEqual(expected_author, 'testuser')
        self.assertEqual(expected_thread, 'Test Thread')
        self.assertEqual(expected_content, 'This is a test post')

    def test_post_with_image(self):
        image_data = b'\x00' * 1024  # 1KB dummy image data
        image_file = SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg')
        post_with_image = Post.objects.create(
            author=self.user,
            thread=self.thread,
            content='This is a test post with image',
            image=image_file
        )
        self.assertTrue(post_with_image.image)
        self.assertEqual(post_with_image.content, 'This is a test post with image')
    
class PostViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.thread_user = User.objects.create_user(username='threaduser', password='54321')
        self.topic = Topic.objects.create(title='Test Topic')
        self.thread = Thread.objects.create(title='Test Thread', author=self.thread_user, topic=self.topic)
        self.post = Post.objects.create(
            author=self.user,
            thread=self.thread,
            content='This is a test post'
        )
    
    def test_post_list_view(self):
        url = reverse('view-thread', kwargs={"topic_id": self.topic.id, "thread_id": self.thread.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test post')
        self.assertTemplateUsed(response, 'forum/thread_post_list.html')
    
    def test_create_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post-create', kwargs={"topic_id": self.topic.id, "thread_id": self.thread.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_form.html')

        response = self.client.post(reverse('post-create', kwargs={"topic_id": self.topic.id, "thread_id": self.thread.id}), {
            'content': 'New post text',
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Post.objects.filter(content='New post text').exists())
    
    def test_create_post_view_with_invalid_image_format(self):
        invalid_image_data = b'this is not real image data'
        invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
        form = CommentCreateForm(files={'image': invalid_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())

    def test_create_post_with_oversized_image(self):
        oversized_image_data = b'\x00' * 10485760 
        oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
        form = CommentCreateForm(files={'image': oversized_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())

    def test_update_post_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('post-update', kwargs={"pk": self.post.pk, "topic_id": self.topic.id, "thread_id": self.thread.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_form.html')

        self.assertEqual(self.post.content, 'This is a test post')

        response = self.client.post(url, {
            'content': 'Updated text',
        })
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.content, 'Updated text')
    
    def test_delete_post_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('post-delete', kwargs={"pk": self.post.pk, "topic_id": self.topic.id, "thread_id": self.thread.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_confirm_delete.html')

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())