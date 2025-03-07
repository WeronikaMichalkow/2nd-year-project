from django.shortcuts import render, redirect
from django.views import View
from .models import Review
from .forms import ReviewForm

class ReviewsView(View):
    def get(self, request):
        reviews = Review.objects.all()  # Fetch all reviews
        form = ReviewForm()  
        return render(request, 'reviews/reviews.html', {'reviews': reviews, 'form': form})

    def post(self, request):
        if request.user.is_authenticated:  
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user  
                review.save()
                return redirect('reviews')  
            return redirect('accounts:signin')  
