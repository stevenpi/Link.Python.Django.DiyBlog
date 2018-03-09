from django.shortcuts import render
from .models import Post, Comment


# Create your views here.
from django.views import generic


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5
