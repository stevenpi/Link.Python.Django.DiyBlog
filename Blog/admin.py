from django.contrib import admin
from .models import Post, Comment

admin.site.register(Comment)


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
