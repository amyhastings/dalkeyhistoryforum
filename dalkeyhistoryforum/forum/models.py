from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image

User = get_user_model()

class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    pinned = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('view-thread', args=[str(self.topic.id), str(self.id)]) 

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_pics', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and hasattr(self.image, 'path'):
            with Image.open(self.image.path) as img:
                if img.width > 600 or img.height > 600:
                    output_size = (600, int((600 / img.width) * img.height))
                    img = img.resize(output_size, Image.LANCZOS)
                    img.save(self.image.path)

