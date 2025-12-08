from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import LoginForm, UserProfileForm, SignUpForm

class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('offers:offer_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard(request):
    """
    Routeur de redirection après connexion :
    1. SUPERUSER (Admin) -> Dashboard Statistique
    2. STAFF (Enseignant) -> Liste des offres en attente (Outil de travail)
    3. AUTRE (Étudiant) -> Mes candidatures
    """
    if request.user.is_superuser:
        # C'est le seul qui a le droit au dashboard
        return redirect('dashboard:admin_dashboard')
        
    elif request.user.is_staff:
        # L'enseignant a accès à tout (admin, validation) sauf dashboard
        # On le redirige vers la liste des validations
        return redirect('offers:offer_pending_list')
        
    else:
        # Étudiant
        return redirect('offers:my_applications')

def logout_view(request):
    logout(request)
    return redirect('offers:offer_list')