from django.conf import settings

from celery import shared_task
from .signals import send_notifications
from .models import Post, Category

import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@shared_task
def notify_about_new_post(pid):
    post = Post.objects.get(pk = pid)
    categories = post.categories.all()
    subscribers: list[str] = []

    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]

    send_notifications(post.preview, post.pk, post.header, subscribers)

@shared_task
def eweek_sender():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'posts': posts,
            'link': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()