from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import LoginForm, UserProfileForm, SignUpForm
from apps.offers.models import InternshipOffer, Application

class LoginView(DjangoLoginView):
    """Vue d'authentification utilisée par accounts/urls.py"""
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

# Si tu gardes une vue fonctionnelle existante, laisse-la inchangée :
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('offers:offer_list')
        messages.error(request, "Identifiants invalides.")
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})

class ProfileView(LoginRequiredMixin, UpdateView):
    """Édition du profil utilisateur (utilisé par accounts/urls.py)."""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard(request):
    # if user is staff show all offers, else show user applications
    if request.user.is_staff:
        offers = InternshipOffer.objects.order_by('-submission_date')
        return render(request, 'accounts/dashboard.html', {'offers': offers, 'is_staff': True})
    else:
        applications = Application.objects.filter(student_email=request.user.email).order_by('-application_date')
        return render(request, 'accounts/dashboard.html', {'applications': applications, 'is_staff': False})



def logout_view(request):
    """
    Déconnexion simple en GET puis redirection vers la page d'accueil.
    """
    logout(request)
    return redirect('offers:offer_list')  # ou 'login' si tu préfères
