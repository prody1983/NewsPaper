import django_filters
from django_filters import FilterSet
from .models import Post
from django import forms

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):

   # Фильтр по дате публикации
   time_create = django_filters.DateTimeFilter(
       field_name='time_create',
       widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
       label='Начиная с даты:',
       lookup_expr='gt'
   )

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'header': ['icontains'],
           # по имени автора
           'author_ref__user_ref__username': ['icontains'],
       }
