from django.db import models
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