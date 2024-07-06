from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    BOOK_CATEGORY = [
        ('1', 'kids'),
        ('2', 'teenagers'),
        ('3', 'adults'),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=BOOK_CATEGORY, default='1')
    year = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default='available')

    def __str__(self):
        return f'{self.author.name} "{self.title}"'

    def get_category_display(self):
        return dict(self.BOOK_CATEGORY).get(self.category, 'Unknown')


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.book.author.name} "{self.book.title}" rented by {self.user.username}'
