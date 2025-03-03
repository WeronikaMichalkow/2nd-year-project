from django.shortcuts import render, redirect
from django.views import View
from .models import Review
from .forms import ReviewForm

class ReviewsView(View):
    def get(self, request):
        reviews = Review.objects.all()  # Fetch all reviews
        form = ReviewForm()  # Initialize an empty form
        return render(request, 'reviews/reviews.html', {'reviews': reviews, 'form': form})

    def post(self, request):
        if request.user.is_authenticated:  # Ensure user is logged in
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user  # Attach the current user to the review
                review.save()
                return redirect('reviews')  # Redirect to the reviews page
        else:
            return redirect('accounts:signin')  # Redirect to login page if not authenticated
