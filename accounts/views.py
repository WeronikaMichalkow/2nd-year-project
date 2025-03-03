from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.views import LogoutView
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, SignInForm  # Ensure SignInForm exists
from django.urls import reverse_lazy

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('/')  # ✅ Redirecting to home page

        for error in form.errors.values():
            for err in error:
                messages.error(request, err)

        return render(request, 'signup.html', {'form': form})

class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'sign_in.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next') or '/')  # ✅ Redirects to home
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'sign_in.html', {'form': form})

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = reverse_lazy('/')  # Redirect to home after logout

class ChangePasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        return render(request, 'change_password.html', {'form': form})

