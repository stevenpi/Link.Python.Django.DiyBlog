from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import Model


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


class Comment(ContentModelMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20] + "..."
