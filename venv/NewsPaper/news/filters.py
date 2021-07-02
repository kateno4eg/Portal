import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(django_filters.FilterSet):
    post_created_on = django_filters.DateFilter(field_name='post_created_on',lookup_expr='gt')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Post
        fields = ('title', 'author', 'post_created_on')
