from django.db import models
from django.contrib.auth.models import User
from .llama3_model import GenerateSummary
from django.core.exceptions import ValidationError
from django.db.models import Avg


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
    aggregated_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate the summary before saving
        summary = GenerateSummary()
        self.summary = summary.generate_summary(self.title + " " + self.author)
        super(Books, self).save(*args, **kwargs)

    def update_aggregated_rating(self):
        # Calculate the average rating of all reviews for this book
        reviews = self.book_ref.all()
        if reviews.exists():
            self.aggregated_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            self.aggregated_rating = None
        self.save()


class Review(models.Model):
    """
    reviews table with the following fields: id, book_id (foreign key 
    referencing books), user_id, review_text, rating.
    """
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='book_ref')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ref')
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.username}'
    
    def save(self, *args, **kwargs):
        if self.rating < 1.0 or self.rating > 5.0:
            raise ValidationError("Rating must be between 1.0 and 5.0.")
        super().save(*args, **kwargs)
        self.book.update_aggregated_rating()


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_genres = models.CharField(max_length=255, blank=True)
    preferred_authors = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
