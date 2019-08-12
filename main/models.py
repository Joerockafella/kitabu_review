from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


#one to many relationship to be changed

class Book(models.Model):
    isbn = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    review = models.ManyToManyField('Post', related_name="review")

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk':self.pk} )

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk} )
