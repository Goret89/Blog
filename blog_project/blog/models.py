from django.db import models
import markdown
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self):
        return self.title

    def get_markdown(self):
        return mark_safe(markdown.markdown(self.content))

    def likes_count(self):
        return self.votes.filter(value=1).count()

    def dislikes_count(self):
        return self.votes.filter(value=-1).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_markdown(self):
        return mark_safe(markdown.markdown(self.content))


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VALUE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)

    class Meta:
        unique_together = ('user', 'post') # duplicate protection


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
