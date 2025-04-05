from django.urls import path
from .views import ReviewsView, SubmitReviewView, delete_review

urlpatterns = [
    path('', ReviewsView.as_view(), name='reviews'),  
    path('submit/', SubmitReviewView.as_view(), name='submit_review'),
    path('delete/<int:review_id>/', delete_review, name='delete_review'),
]
