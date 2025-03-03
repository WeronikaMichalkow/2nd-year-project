from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'placeholder': 'Add your review', 'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-control'}),  # Ratings 1 to 5
        }
