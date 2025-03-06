from django.urls import path
from .views import mens_view, category_view, kids_view

urlpatterns = [
    path('store/men/', mens_view, name='mens_page'),
    path('store/<str:main_category>/', category_view, name='category_page'),
    path('store/kids/', kids_view, name='kids_page'),
    
]