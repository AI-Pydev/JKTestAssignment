import joblib
import pandas as pd
from django.http import JsonResponse
from django.views import View
from .models import Books, Review
from .llama3_model import GenerateSummary
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors



class SummarizeBookView(View):
    def get(self, request, book_id):
        try:
            summary = GenerateSummary()
            book = Books.objects.get(id=book_id)
            summary = summary.generate_summary(book.title + " " + book.author)
            return JsonResponse({'summary': summary})
        except Books.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

class SummarizeReviewView(View):
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            summary = summary.generate_summary(review.review_text)
            return JsonResponse({'summary': summary})
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)

