from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Review
from .forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from store.models import Product

class ReviewsView(View):
    def get(self, request):
        reviews = Review.objects.all()  
        form = ReviewForm()  
        return render(request, 'reviews/reviews.html', {'reviews': reviews, 'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
               
                review.product = form.cleaned_data.get('product')
                review.save()
                return redirect('reviews')
        return redirect('cos_accounts:signin')
        
@method_decorator(csrf_exempt, name='dispatch')
class SubmitReviewView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('cos_accounts:signin')

        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        product_id = request.POST.get('product')

        
        product = get_object_or_404(Product, id=product_id)

     
        if review_text and rating:
            Review.objects.create(
                user=request.user,
                product=product, 
                review_text=review_text,
                rating=rating
            )

        return redirect(request.META.get('HTTP_REFERER', '/'))