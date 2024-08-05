# books/urls.py
from django.urls import path
from .views import SummarizeBookView, SummarizeReviewView

urlpatterns = [
    path('summarize/book/<int:book_id>/', SummarizeBookView.as_view(), name='summarize_book'),
    path('summarize/review/<int:review_id>/', SummarizeReviewView.as_view(), name='summarize_review'),
]
