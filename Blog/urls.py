from django.urls import path
from django.conf import settings

from Blog.Feeds.blogpost_feed import LatestPostsFeed
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.post_detail_view, name="post-detail"),
    path('comments/<int:pk>/add', views.add_comment_form, name="comment-add"),
    path('comments/<int:pk>/do-add', views.add_comment, name="comment-add-do"),
    path('posts/add', views.PostCreate.as_view(), name="post-add"),
    path('vote', views.vote_content_model, name="vote"),
    path('users/', views.UserListView.as_view(), name="users"),
    path('user/<int:pk>', views.user_detail_view, name="user-detail"),
    path('latest/feed/', LatestPostsFeed(), name="feed"),
    path('settings/', views.settings, name="settings"),
]

if settings.DEBUG:
    urlpatterns += [
        path('insert/', views.insert_to_db),
    ]
