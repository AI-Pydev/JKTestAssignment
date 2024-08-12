from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics
from books.models import Books, Review, UserPreference 
from rest_framework.views import APIView
from .serializers import BookSerializer, ReviewSerializer, UserPreferenceSerializer
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from books.llama3_model import GenerateSummary


class BookListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Books.objects.all()  
    serializer_class = BookSerializer  


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()  
    serializer_class = BookSerializer


class ReviewListCreateView(APIView):
    def post(self, request, pk):
        book = Books.objects.get(pk=pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        reviews = Review.objects.filter(book_id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    

class BookSummaryView(APIView):
    def get(self, request, pk):
        try:
            book = Books.objects.get(pk=pk)
            return Response({
                "summary": book.summary,
                "aggregated_rating": book.aggregated_rating
            })
        except Books.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        

class RecommendationsView(APIView):
    def get(self, request):
        user = request.user
        try:
            preferences = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            return Response({"detail": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

        recommended_books = Books.objects.filter(
            Q(genre__in=preferences.preferred_genres.split(',')) |
            Q(author__in=preferences.preferred_authors.split(','))
        ).distinct()

        books_serializer = BookSerializer(recommended_books, many=True)
        return Response(books_serializer.data, status=status.HTTP_200_OK)
    

class UserPreferenceView(APIView):
    def get(self, request):
        user = request.user
        try:
            preferences = UserPreference.objects.get(user=user)
            serializer = UserPreferenceSerializer(preferences)
            return Response(serializer.data)
        except UserPreference.DoesNotExist:
            return Response({"detail": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        try:
            preferences = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            preferences = UserPreference(user=user)

        serializer = UserPreferenceSerializer(preferences, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GenerateSummaryView(APIView):
    def post(self, request, *args, **kwargs):
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        summary = GenerateSummary()
        summary_txt = summary.generate_summary(content)
        return Response({'summary': summary_txt}, status=status.HTTP_200_OK)