import datetime
import random
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.views import generic
from django.urls import reverse
from taggit.models import Tag
from vote.managers import UP

from .models import Post, Comment, Profile
from Blog.blogForms import PostCreateForm, UpdateUserForm, UpdateProfileForm


def _add_pagination_if_needed(context):
    if context.get('is_paginated', True):
        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
    return context


def index(request):
    return render(request, 'index.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()
        forms = [user_form, profile_form]
        messages.success(request, _("Your Profile has been updated."))
    else:
        user = User.objects.get(pk=request.user.id)
        profile = Profile.objects.get(user=user)
        forms = [UpdateUserForm(instance=user), UpdateProfileForm(instance=profile)]
    return render(request, 'Blog/profile_update.html', {'forms': forms})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bio = form.cleaned_data.get('bio')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Blog/signup.html', {'form': form})


class PostListView(generic.ListView):
    model = Post
    paginate_by = 8

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
        context = _add_pagination_if_needed(context)
        return context


class UserListView(generic.ListView):
    model = User
    paginate_by = 8
    template_name = 'Blog/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = _add_pagination_if_needed(context)
        return context


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
        return post_detail_view(request, comment.post.slug)
    return index(request)


@login_required
def vote_content_model(request):
    if request.method != "GET":
        return index(request)

    content_model_id = request.GET.get("model_id", 0)
    if content_model_id == 0:
        return index(request)

    content_types = {"post": "post", "comment": "comment"}
    content_type = request.GET.get("model_type", "")
    if content_type not in content_types:
        return index(request)

    if content_type == content_types["post"]:
        entity = Post.objects.get(pk=content_model_id)
    else:
        entity = Comment.objects.get(pk=content_model_id)

    voted = False
    if entity.votes.exists(request.user.id):
        voted = True

    vote_direction = request.GET.get("like", "")
    if vote_direction == "True" and voted is False:
        entity.votes.up(request.user.id)
    elif vote_direction == "False" and voted is False:
        entity.votes.down(request.user.id)

    if content_type == content_types["post"]:
        return HttpResponseRedirect(reverse('post-detail', kwargs={"slug": entity.slug}))
    else:
        return HttpResponseRedirect(reverse('post-detail', kwargs={"slug": entity.post.slug}))


def user_detail_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    liked_posts = Post.votes.all(user.pk, action=UP)
    context = {'user': user, 'posts': posts, 'comments': comments, 'liked_posts': liked_posts}
    return render(request, 'Blog/user_detail.html', context)


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    comment_add_url = "{}/add".format(request.get_full_path())
    context = {'post': post, 'comments': comments, 'comment_url': comment_add_url}
    return render(request, 'Blog/post_detail.html', context)


def _create_post_slug(post_instance):
    slug = slugify(post_instance.title)
    same_slugs_count = Post.objects.filter(slug__icontains=slug).count()
    if 0 < same_slugs_count:
        # whitespace to let slugify create a hyphen
        slug += "-" + str(same_slugs_count)
    post_instance.slug = slug
    return post_instance


class PostCreate(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreateForm
    template_name = 'Blog/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created = datetime.datetime.now()
        form.instance = _create_post_slug(form.instance)
        return super().form_valid(form)


# Inserts a lot of users, posts and comments to the db
def insert_to_db(request):
    if not request.user.is_superuser:
        raise Http404()

    blogpost_content = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'
    comment_content = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyamLorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam'

    for user_count in range(100):
        user = User()
        user.username = "test-username-{}".format(str(uuid4()))
        user.first_name = "test-first-{}".format(str(uuid4()))
        user.last_name = "test-last-{}".format(str(uuid4()))
        user.save()
        user.refresh_from_db()
        for blogpost_user_count in range(random.randint(1, 30)):
            post = Post()
            post.created = datetime.datetime.now()
            post.title = "title-{}".format(str(uuid4()))
            post.content = blogpost_content
            post.user = user
            post = _create_post_slug(post)
            post.save()
            post.refresh_from_db()
            post.tags.add(str(random.randint(1, 10)))
            for blogpost_comment_count in range(random.randint(1, 20)):
                comment = Comment()
                comment.content = comment_content
                comment.user = user
                comment.created = datetime.datetime.now()
                comment.post = post
                comment.save()
    return index(request)
