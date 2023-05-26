from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts = self.post_set.all()
        for p in posts:
            p1 = Post()
            p1 = p
            self.user_rating = self.user_rating + p1.article_rating*3
            com_posts = p.comment_set.all()
            for cp in com_posts:
                cp1 = Comment()
                cp1 = cp
                self.user_rating = self.user_rating + cp1.comment_rating

        comments = self.comment_set.all()
        for c in comments:
            c1 = Comment()
            c1 = c
            self.user_rating = self.user_rating + c1.comment_rating

        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):
    author_ref = models.ForeignKey(Author, on_delete=models.CASCADE)
    a_or_n = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    article_text = models.TextField()
    article_rating = models.IntegerField(default=0)

    def like(self):
        self.article_rating = self.article_rating + 1
        self.save()

    def dislike(self):
        self.article_rating = self.article_rating - 1
        self.save()

    @property
    def preview(self):
        return self.article_text[0:124]+'...'

    def __str__(self):
        return f'{self.header.title()}: {self.article_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_ref = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating = self.comment_rating + 1
        self.save()

    def dislike(self):
        self.comment_rating = self.comment_rating - 1
        self.save()