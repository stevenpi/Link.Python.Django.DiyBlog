import datetime
import random
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from taggit.models import Tag

from Blog.blogForms import PostCreateForm
from .models import Post, Comment


# Create your views here.
from django.views import generic


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()

        tag = self.request.GET.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__name__in=[tag])

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['current_tag'] = self.request.GET.get('tag', '')
        return context


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


class PostCreate(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreateForm
    template_name = 'Blog/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created = datetime.datetime.now()
        return super().form_valid(form)

# Inserts a lot of users, posts and comments to the db
# def insert_to_db(request):
#     blogpost_content = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'
#     comment_content = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyamLorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam'
#
#     for user_count in range(100):
#         user = User()
#         user.username = "test-username-{}".format(str(uuid4()))
#         user.first_name = "test-first-{}".format(str(uuid4()))
#         user.last_name = "test-last-{}".format(str(uuid4()))
#         user.save()
#         user.refresh_from_db()
#         for blogpost_user_count in range(random.randint(1, 30)):
#             post = Post()
#             post.created = datetime.datetime.now()
#             post.title = "title-{}".format(str(uuid4()))
#             post.content = blogpost_content
#             post.user = user
#             post.save()
#             post.refresh_from_db()
#             post.tags.add(str(random.randint(1, 10)))
#             for blogpost_comment_count in range(random.randint(1, 20)):
#                 comment = Comment()
#                 comment.content = comment_content
#                 comment.user = user
#                 comment.created = datetime.datetime.now()
#                 comment.post = post
#                 comment.save()
#     return index(request)


