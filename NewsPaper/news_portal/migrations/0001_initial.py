# Generated by Django 4.1.7 on 2023-03-14 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rating', models.IntegerField(default=0)),
                ('user_ref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_or_n', models.BooleanField(default=False)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('header', models.CharField(max_length=255)),
                ('article_text', models.TextField()),
                ('article_rating', models.IntegerField(default=0)),
                ('author_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.category')),
                ('post_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(through='news_portal.PostCategory', to='news_portal.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_text', models.TextField()),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('comment_rating', models.IntegerField(default=0)),
                ('post_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.post')),
                ('user_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
