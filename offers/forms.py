from django import forms
from .models import InternshipOffer, Application


class OfferForm(forms.ModelForm):
    """Formulaire utilisé pour le dépôt d'une offre (par entreprise)."""

    class Meta:
        model = InternshipOffer
        fields = ["title", "organization", "contact_name", "contact_email", "details"]
        # statut non modifiable ici → forcer "pending" dans la vue


class ApplicationForm(forms.ModelForm):
    """Formulaire de candidature pour un étudiant connecté."""

    class Meta:
        model = Application
        fields = ["student_name", "student_email"]
