from django.urls import path
from .views import mens_view, category_view

urlpatterns = [
    path('store/men/', mens_view, name='mens_page'),
    path('store/<str:main_category>/', category_view, name='category_page'),
]