from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Books(models.Model):
    """
    books table with the following fields: id, title, author, genre, 
    year_published, summary.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    year_published = models.IntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    """
    reviews table with the following fields: id, book_id (foreign key 
    referencing books), user_id, review_text, rating.
    """
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='book_ref')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ref')
    review_text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.username}'