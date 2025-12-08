from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from django.http import Http404

from .forms import OfferForm, ApplicationForm
from .models import InternshipOffer, Application


def offer_list(request):
    """
    Page d'accueil : liste des offres.
    - Staff : voit toutes les offres.
    - Autres : voient SEULEMENT les offres validées (pas les clôturées).
    """
    q = request.GET.get("q", "").strip()

    if request.user.is_authenticated and request.user.is_staff:
        offers = InternshipOffer.objects.all()
    else:
        # --- CORRECTION STRICTE ---
        # Le cahier des charges dit : "n’apparaît plus dans la liste des offres en cours"
        # On ne sélectionne donc QUE 'validated'.
        offers = InternshipOffer.objects.filter(status="validated")

    if q:
        offers = offers.filter(
            models.Q(title__icontains=q)
            | models.Q(organization__icontains=q)
            | models.Q(details__icontains=q)
        )

    offers = offers.order_by('-submission_date')

    return render(
        request,
        "offers/offer_list.html",
        {
            "offers": offers,
            "query": q,
        },
    )


def offer_detail(request, pk):
    """
    Détail d'une offre.
    """
    offer = get_object_or_404(InternshipOffer, pk=pk)

    # Sécurité : 
    # On autorise 'validated' ET 'closed' pour que l'étudiant qui vient de prendre
    # la 5ème place ne tombe pas sur une erreur 404 après sa redirection.
    visible_statuses = ['validated', 'closed']
    
    is_staff = request.user.is_authenticated and request.user.is_staff
    
    # Si l'offre est en attente ou rejetée, et qu'on n'est pas staff -> 404
    if offer.status not in visible_statuses and not is_staff:
        raise Http404("Cette offre n'est pas disponible.")

    # Logique pour le bouton "Postuler"
    is_student = request.user.is_authenticated and not request.user.is_staff
    can_apply = offer.is_open_for_applications and is_student

    context = {
        "offer": offer,
        "applications_count": offer.applications_count,
        "can_apply": can_apply,
    }
    return render(request, "offers/offer_detail.html", context)


def offer_create(request):
    # Si l'utilisateur est connecté MAIS n'est pas staff -> BLOQUER
    if request.user.is_authenticated and not request.user.is_staff:
        messages.info(request, "Espace étudiant : vous ne pouvez pas déposer d'offres de stage.")
        return redirect("offers:offer_list")

    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.status = "pending"
            offer.save()
            
            messages.success(request, "L'offre a bien été déposée et sera examinée prochainement.")

            if request.user.is_authenticated and request.user.is_staff:
                return redirect("offers:offer_detail", pk=offer.pk)
            
            return redirect("offers:offer_list")
    else:
        form = OfferForm()

    return render(
        request,
        "offers/offer_form.html",
        {"form": form, "offer": None},
    )


@login_required
def offer_apply(request, pk):
    offer = get_object_or_404(InternshipOffer, pk=pk)

    # Offre encore ouverte ?
    if not offer.is_open_for_applications:
        messages.error(request, "Cette offre n'est plus ouverte aux candidatures.")
        return redirect("offers:offer_detail", pk=offer.pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # 1. Vérif quota avant sauvegarde
            if offer.applications.count() >= 5:
                offer.status = "closed"
                offer.save(update_fields=["status"])
                messages.error(request, "Le quota de 5 candidatures est déjà atteint.")
                return redirect("offers:offer_detail", pk=offer.pk)

            application = form.save(commit=False)
            application.offer = offer

            if request.user.is_authenticated:
                application.student_name = request.user.get_full_name() or request.user.username
                application.student_email = request.user.email

            try:
                application.save()
            except Exception:
                messages.error(request, "Erreur : Vous avez déjà candidaté à cette offre.")
                return redirect("offers:offer_detail", pk=offer.pk)

            # 2. Re-vérification quota APRÈS sauvegarde pour fermer l'offre immédiatement
            if offer.applications.count() >= 5:
                offer.status = "closed"
                offer.save(update_fields=["status"])

            messages.success(request, "Votre candidature a bien été enregistrée.")
            return redirect("offers:offer_detail", pk=offer.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "student_name": request.user.get_full_name() or request.user.username,
                "student_email": request.user.email,
            }
        form = ApplicationForm(initial=initial)

    return render(
        request,
        "offers/application_form.html",
        {"form": form, "offer": offer},
    )


def staff_required(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(staff_required)
def offer_pending_list(request):
    offers = InternshipOffer.objects.filter(status="pending").order_by("-submission_date")
    return render(request, "offers/offer_pending_list.html", {"offers": offers})


@login_required
@user_passes_test(staff_required)
def offer_set_status(request, pk, status):
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
    applications = Application.objects.filter(
        student_email=request.user.email
    ).select_related("offer").order_by("-application_date")

    return render(
        request,
        "offers/my_applications.html",
        {"applications": applications},
    )