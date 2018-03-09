from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.PostListView.as_view(), name="post-detail"),
    path('user/<int:pk>', views.user_detail_view, name="user-detail"),
]
