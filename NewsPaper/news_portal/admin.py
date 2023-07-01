from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Comment

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице
    list_display = ('time_create', 'header', 'preview', 'a_or_n', 'article_rating', 'get_author_name')
    list_filter = ('a_or_n', 'article_rating', 'author_ref__user_ref__username') # добавляем примитивные фильтры в нашу админку
    search_fields = ('header', 'categories__name') # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
