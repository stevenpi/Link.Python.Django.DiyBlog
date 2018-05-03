from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from Blog.Feeds.blogpost_feed import LatestPostsFeed
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('post/<slug:slug>', views.post_detail_view, name="post-detail"),
    path('comments/<int:pk>/add', views.add_comment_form, name="comment-add"),
    path('comments/<int:pk>/do-add', views.add_comment, name="comment-add-do"),
    path('posts/add', views.PostCreate.as_view(), name="post-add"),
    path('vote', views.vote_content_model, name="vote"),
    path('users/', views.UserListView.as_view(), name="users"),
    path('user/<username>', views.user_detail_view, name="user-detail"),
    path('profile/edit', views.update_profile, name="profile-update"),
    path('latest/feed/', LatestPostsFeed(), name="feed"),
    path('settings/', views.settings, name="settings"),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('insert/', views.insert_to_db),
    ]
