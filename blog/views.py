from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from blog.models import Post


# Create your views here.

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        posts = cache.get('all_posts')

        if not posts:
            posts = Post.objects.all()
            cache.set('all_posts', posts, 60 * 15)

        return posts


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        self.object.views_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)
