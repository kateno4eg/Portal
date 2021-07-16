from django.shortcuts import render, reverse,redirect
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from django.core.paginator import Paginator
from .models import Post, Author, Category, Comment
from .filters import PostFilter
from .forms import PostForm, UserForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers, mail_admins




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


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/add.html'
    form_class = PostForm


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',)
    template_name = 'news/edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    form_class = UserForm
    success_url = '/profile/'

    def get_object(self, **kwargs):
        id = self.request.user.id
        return User.objects.get(pk=id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class NewsDeleteView(DeleteView):
    template_name = 'news/delete.html'
    context_object_name = 'new'
    queryset = Post.objects.all()
    success_url = '/'

class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'
    paginate_by = 5


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category not in user.category_set.all():
        category.subscribers.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category in user.category_set.all():
        category.subscribers.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))