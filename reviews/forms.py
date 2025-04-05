from django import forms
from .models import Review
from store.models import Product

class ReviewForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False, 
        empty_label="General (No specific product)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Review
        fields = ['product', 'review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'placeholder': 'Add your review', 
                'rows': 4, 
                'class': 'form-control'
            }),
            'rating': forms.Select(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
        }
