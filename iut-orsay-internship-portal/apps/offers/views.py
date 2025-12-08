from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models

from .forms import OfferForm, ApplicationForm
from .models import InternshipOffer, Application


def offer_list(request):
    """
    Page d'accueil : liste des offres

    - Si l'utilisateur est staff/admin : toutes les offres
    - Sinon (anonyme ou étudiant) : seulement les offres validées
    - Recherche par ?q= dans le titre, l'organisme ou le détail
    """
    q = request.GET.get("q", "").strip()

    if request.user.is_authenticated and request.user.is_staff:
        offers = InternshipOffer.objects.all()
    else:
        offers = InternshipOffer.objects.filter(status="validated")

    if q:
        offers = offers.filter(
            models.Q(title__icontains=q)
            | models.Q(organization__icontains=q)
            | models.Q(details__icontains=q)
        )

    return render(
        request,
        "offers/offer_list.html",
        {
            "offers": offers,
            "query": q,
        },
    )



def offer_detail(request, pk):
    """Détail d'une offre."""
    offer = get_object_or_404(InternshipOffer, pk=pk)

    context = {
        "offer": offer,
        "applications_count": offer.applications_count,
        "can_apply": offer.is_open_for_applications,
    }
    return render(request, "offers/offer_detail.html", context)


def offer_create(request):
    """
    Dépôt d'offre par une entreprise (sans login).
    Toutes les nouvelles offres arrivent en 'pending'.
    """
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.status = "pending"  # forcer statut "en attente"
            offer.save()
            messages.success(
                request,
                "Votre offre a bien été déposée. "
                "Elle sera examinée par un responsable des stages.",
            )
            return redirect("offers:offer_detail", pk=offer.pk)
    else:
        form = OfferForm()

    return render(
        request,
        "offers/offer_form.html",
        {"form": form, "offer": None},
    )


@login_required
def offer_apply(request, pk):
    """
    Candidature d'un étudiant à une offre.

    Règles :
    - l'offre doit être ouverte (validated + < 5 candidatures)
    - à partir de 5 candidatures, l'offre passe à 'closed'
    """
    offer = get_object_or_404(InternshipOffer, pk=pk)

    # Offre encore ouverte ?
    if not offer.is_open_for_applications:
        messages.error(request, "Cette offre n'est plus ouverte aux candidatures.")
        return redirect("offers:offer_detail", pk=offer.pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Re-vérifier juste avant de sauvegarder
            if offer.applications.count() >= 5:
                offer.status = "closed"
                offer.save(update_fields=["status"])
                messages.error(
                    request,
                    "Le quota de 5 candidatures est déjà atteint.",
                )
                return redirect("offers:offer_detail", pk=offer.pk)

            application = form.save(commit=False)
            application.offer = offer

            # Pré-remplir avec les infos du compte si besoin
            if request.user.is_authenticated:
                if not application.student_name:
                    application.student_name = (
                        request.user.get_full_name() or request.user.username
                    )
                if not application.student_email:
                    application.student_email = request.user.email

            application.save()

            # Si on vient d'atteindre 5 → on clôture
            if offer.applications.count() >= 5:
                offer.status = "closed"
                offer.save(update_fields=["status"])

            messages.success(request, "Votre candidature a bien été enregistrée.")
            return redirect("offers:offer_detail", pk=offer.pk)
    else:
        # GET → afficher le formulaire
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "student_name": request.user.get_full_name()
                or request.user.username,
                "student_email": request.user.email,
            }
        form = ApplicationForm(initial=initial)

    return render(
        request,
        "offers/application_form.html",
        {"form": form, "offer": offer},
    )


def staff_required(user):
    """Test utilisé pour les vues réservées au responsable/admin."""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(staff_required)
def offer_pending_list(request):
    """
    Liste des offres en attente de validation (pour responsable/admin).
    """
    offers = InternshipOffer.objects.filter(status="pending").order_by(
        "-submission_date"
    )
    return render(
        request,
        "offers/offer_pending_list.html",
        {"offers": offers},
    )


@login_required
@user_passes_test(staff_required)
def offer_set_status(request, pk, status):
    """
    Changer le statut d'une offre :
    - pending -> validated / rejected
    - ou la forcer en closed
    """
    offer = get_object_or_404(InternshipOffer, pk=pk)

    allowed_statuses = {"pending", "validated", "rejected", "closed"}
    if status not in allowed_statuses:
        messages.error(request, "Statut invalide.")
        return redirect("offers:offer_detail", pk=offer.pk)

    offer.status = status
    offer.save(update_fields=["status"])

    messages.success(
        request,
        f"Le statut de l'offre a été mis à jour : {offer.get_status_display()}",
    )
    return redirect("offers:offer_detail", pk=offer.pk)


@login_required
def my_applications(request):
    """
    Liste des candidatures de l'étudiant connecté.
    Filtrage par email de l'utilisateur.
    """
    applications = Application.objects.filter(
        student_email=request.user.email
    ).select_related("offer").order_by("-application_date")

    return render(
        request,
        "offers/my_applications.html",
        {"applications": applications},
    )
