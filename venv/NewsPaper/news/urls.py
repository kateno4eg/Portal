from django.urls import path
from .views import News, Search, NewsCreateView, NewsUpdateView, NewsDeleteView, NewsDetailView

urlpatterns = [
    path('', News.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='new'),
    path('search/', Search.as_view(), name='search'),
    path('add/', NewsCreateView.as_view(), name='add'),
    path('add/<int:pk>', NewsUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='delete'),
]