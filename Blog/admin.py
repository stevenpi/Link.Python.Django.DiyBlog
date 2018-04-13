from django.contrib import admin
from .models import Post, Comment, Profile

admin.site.register(Comment)
admin.site.register(Profile)


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
