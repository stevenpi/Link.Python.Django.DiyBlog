from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.post_detail_view, name="post-detail"),
    path('posts/<int:pk>/add', views.add_comment_form, name="comment-add"),
    path('posts/<int:pk>/do-add', views.add_comment, name="comment-add-do"),
    path('users/', views.UserListView.as_view(), name="users"),
    path('user/<int:pk>', views.user_detail_view, name="user-detail"),
    # url for inserting into the db (lookup on views.py)
    # path('insert/', views.insert_to_db),
]

