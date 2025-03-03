from django.urls import path
from . import views
from .views import CustomLogoutView



app_name = 'accounts'  

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
]