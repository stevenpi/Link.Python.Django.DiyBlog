from django.contrib.auth.models import User
from django.db import models

from django.db.models import Model
from django.urls import reverse


# inject get_absolute_url method to `User` class by Django
def get_absolute_url(self):
    return reverse('user-detail', args=[str(self.username)])


User.get_absolute_url = get_absolute_url


class ContentModelMixin(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=2048)
    created = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Post(ContentModelMixin):
    title = models.CharField(max_length=64, default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    class Meta:
        ordering = ["-created"]


class Comment(ContentModelMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20] + "..."
