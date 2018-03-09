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


def user_detail_view(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'Blog/user_detail.html', context)

