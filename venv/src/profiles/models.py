# To generate random default pic
from random import randint

from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image

# User model
User = get_user_model()


# ****** User Profile Model ******
class Profile(models.Model):
    number = randint(1, 12)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=f'default_imgs/{number}.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{user.username} - Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        # Resizing the image for better performance
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
