from django.contrib import admin
from .models import Books, Review
from .llama3_model import generate_summary


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year_published')

    def save_model(self, request, obj, form, change):
        if not change:  # Only generate summary when a new book is added
            obj.summary = generate_summary(obj.title + " " + obj.author)  # Adjust the content used for summary
        super().save_model(request, obj, form, change)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Optionally, you can generate a summary of the review text as well
