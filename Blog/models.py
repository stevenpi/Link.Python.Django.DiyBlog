from django.contrib.auth.models import User
from django.db import models

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


from vote.models import VoteModel
from taggit.managers import TaggableManager


class ContentModelMixin(VoteModel, models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=2048)
    created = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ["-created"]


class Post(ContentModelMixin):
    title = models.CharField(max_length=64, default="")
    tags = TaggableManager()
    slug = models.SlugField(default='', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.slug)])


class Comment(ContentModelMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:75] + "..."


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1024, blank=True)
    image = models.ImageField(blank=True)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user.username)])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
