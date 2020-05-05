from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField
# https://docs.djangoproject.com/en/3.0/ref/models/fields/

class Post(models.Model):
    title = models.TextField(blank=True, null=True)
    # image = models.ImageField()
    image = ProcessedImageField(
        upload_to='static/image/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)]) # jump to name=post_detail in url.py


class InstagramUser(AbstractUser):
    profile_picture = ProcessedImageField(
        upload_to='static/image/profiles',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )