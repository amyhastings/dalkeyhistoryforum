from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

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
    image = models.ImageField(
        upload_to='post_pics',
        storage=MediaCloudinaryStorage(),
        null=True, 
        blank=True,
    )

    def get_image_url(self):
        if self.image and hasattr(self.image, 'path'):
            return cloudinary_url(self.image.name, width=600)[0]