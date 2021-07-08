from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.core.paginator import Paginator
from .models import Post, Author, Category, Comment
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-post_created_on']
    paginate_by = 4


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-post_created_on']

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset())
        return context

class NewsDetailView(DetailView):
    template_name = 'news/new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()


class NewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news/add.html'
    form_class = PostForm


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news/delete.html'
    context_object_name = 'new'
    queryset = Post.objects.all()
    success_url = '/news/'

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'
    

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')