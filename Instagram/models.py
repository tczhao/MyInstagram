from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField
# https://docs.djangoproject.com/en/3.0/ref/models/fields/


class InstagramUser(AbstractUser):
    profile_picture = ProcessedImageField(
        upload_to='static/image/profiles',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username
        
class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username


class Post(models.Model):
    author = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name='my_post'
    )
    title = models.TextField(blank=True, null=True)
    # image = models.ImageField()
    image = ProcessedImageField(
        upload_to='static/image/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )
    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.title

    def get_like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)]) # jump to name=post_detail in url.py

    def get_comment_count(self):
        return self.comments.count()


class Like(models.Model): # contains 2 fields
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ("post", "user") # 1 to 1 unique mapping

    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        InstagramUser,
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment
