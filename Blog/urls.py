from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.post_detail_view, name="post-detail"),
    path('users/', views.UserListView.as_view(), name="users"),
    path('user/<int:pk>', views.user_detail_view, name="user-detail"),

]

