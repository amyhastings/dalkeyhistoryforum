from django.db import models
from django.contrib.auth.models import User

from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_pics',
        storage=MediaCloudinaryStorage(),
        null=True, 
    )

    def get_image_url(self):
        if self.image: 
            if settings.STORAGES == 'cloudinary_storage.storage.MediaCloudinaryStorage':
                return cloudinary_url(self.image.name, width=300, height=300, crop="lfill")[0]
            else:
                return self.image.url
        else: 
            return static('users/default.jpg')
