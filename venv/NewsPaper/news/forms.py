from django.forms import ModelForm,TextInput
from .models import Post
from allauth.account.forms import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author','title', 'post_type', 'category', 'article_text']


class UserForm(ModelForm):
    username = forms.CharField(label='Логин пользователя', widget=forms.TextInput())
    first_name = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия пользователя', widget=forms.TextInput())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user