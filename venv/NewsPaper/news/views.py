from django.views.generic import ListView, DetailView
from .models import Author, Post, Category, PostCategory, Comment

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-post_created_on')


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
