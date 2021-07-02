from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.author_rating = pRat * 3 + cRat
        self.save()
        return self.author_rating

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

class Post(models.Model):

    post = 'AR'
    news = 'NE'

    POST_TYPES = [
        (post, 'Пост'),
        (news, 'Новость')
        ]

    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=post)
    post_created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    article_text = models.TextField(blank=True)
    post_rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')


    def like(self):
        self.post_rating += 1
        self.save()
        return self.post_rating

    def dislike(self):
        self.post_rating -= 1
        self.save()
        return self.post_rating

    def preview(self):
        preview = self.article_text[:124]
        return f'{preview} + "..."'

    def __str__(self):
        return self.title + ', Автор: ' + self.author.user.username

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created_on = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)


    def like(self):
        self.comment_rating += 1
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1
        self.save()
        return self.comment_rating

    def __str__(self):
        return 'Пост: ' + self.post.title + ', Пользователь: ' + self.user.username
