import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Post, Comment


# Create your views here.
from django.views import generic


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class UserListView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'Blog/user_list.html'


@login_required
def add_comment_form(request, pk):
    post = Post.objects.get(pk=pk)
    do_add_url = request.build_absolute_uri().replace('add', 'do-add')
    context = {'blogpost': post, 'do_add_url': do_add_url, }
    return render(request, 'Blog/comment_add.html', context)


@login_required()
def add_comment(request, pk):
    if request.method == "POST":
        content = request.POST.get("content", "")
        comment = Comment()
        comment.user = request.user
        comment.post = Post.objects.get(pk=pk)
        comment.created = datetime.datetime.now()
        comment.content = content
        comment.save()
        return post_detail_view(request, pk)
    return index(request)


def user_detail_view(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'Blog/user_detail.html', context)


def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    comment_add_url = "{}/add".format(request.get_full_path())
    context = {'post': post, 'comments': comments, 'comment_url': comment_add_url}
    return render(request, 'Blog/post_detail.html', context)

