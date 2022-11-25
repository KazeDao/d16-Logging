from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_author_posts = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        rating_author_comments = self.user.comment_set.all().aggregate(Sum('comm_rating'))['comm_rating__sum']
        all_comm_rating = self.post_set.all().aggregate(Sum('comment__comm_rating'))['comment__comm_rating__sum']
        self.rating = rating_author_posts + rating_author_comments + all_comm_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name.title()


CHOICES = [('news', 'Новости'), ('articles', 'Статьи')]


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=CHOICES, default='news')
    post_time = models.DateTimeField(auto_now_add=True)
    post_categories = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=50)
    post_text = models.TextField(blank=True)
    post_rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.post_title.title()}: {self.post_text[:20]}'

    def like_post(self):
        self.post_rating += 1
        self.save()

    def dislike_post(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:123] + "..."

    def get_absolute_url(self):
        return reverse("new", kwargs={"pk": self.pk})


class PostCategory(models.Model):
    pc_name = models.CharField(max_length=20)
    pc_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pc_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comm_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField(blank=True)
    comm_time = models.DateTimeField(auto_now_add=True)
    comm_rating = models.FloatField(default=0.0)

    def like_comm(self):
        self.comm_rating += 1
        self.save()

    def dislike_comm(self):
        self.comm_rating -= 1
        self.save()
