import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post
from django.conf import settings


@shared_task
def celery_weekly_mails():
    time_delta = datetime.timedelta(7)
    start = datetime.datetime.utcnow() - time_delta
    end = datetime.datetime.utcnow()

    posts = Post.objects.filter(created_at__range=(start, end))
    users = User.objects.all()
    emails = [user.email for user in users]
    html_content = render_to_string('account/email/weekly_posts_mail', {'posts': posts},)
    msg = EmailMultiAlternatives(
        subject=f'"Еженедельная рассылка(celery)"',
        body="Статьи и Новости",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
