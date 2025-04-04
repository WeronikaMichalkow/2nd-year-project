from django import forms
from .models import Review , Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),  # Add this
            'review_text': forms.Textarea(attrs={'placeholder': 'Add your review', 'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-control'}),  
        }
