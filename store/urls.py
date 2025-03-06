from django.urls import path
from . import views

urlpatterns = [
    path('store/men/', views.mens_view, name='mens_view'),
    path('store/<str:main_category>/', views.category_view, name='category_view'),
]
