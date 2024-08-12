from django.urls import path
from .views import BookListCreateView, BookDetailView, \
    ReviewListCreateView, BookSummaryView, UserPreferenceView, RecommendationsView, GenerateSummaryView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/reviews/', ReviewListCreateView.as_view(), name='book-reviews'),
    path('books/<int:pk>/summary/', BookSummaryView.as_view(), name='book-summary'),
    path('preferences/', UserPreferenceView.as_view(), name='user-preferences'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    path('generate-summary/', GenerateSummaryView.as_view(), name='generate-summary'),
]