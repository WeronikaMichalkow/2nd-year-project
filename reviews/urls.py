from django.urls import path
from .views import ReviewsView, SubmitReviewView

urlpatterns = [
    path('', ReviewsView.as_view(), name='reviews'),  
    path('submit/', SubmitReviewView.as_view(), name='submit_review'),
]
