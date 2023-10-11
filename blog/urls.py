from django.urls import path

from blog.views import PostListView, PostDetailView
from service.views import *

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
