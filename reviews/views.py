from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Review
from .forms import ReviewForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse

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



@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("You can't delete someone else's review.")

    review.delete()
    return redirect('reviews')

def like_test(request):
    review = Review.objects.first()  
    return render(request, 'reviews/like_test.html', {'review': review})

@csrf_exempt
def test_like_review(request, review_id):
    if request.method == 'POST':
        review = Review.objects.get(id=review_id)
        review.helpful_count += 1
        review.save()
        return JsonResponse({'helpful_count': review.helpful_count})
    return JsonResponse({'error': 'Invalid method'}, status=400)

@csrf_exempt
def like_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            review.helpful_count += 1
            review.save()
            return JsonResponse({'helpful_count': review.helpful_count})
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=400)