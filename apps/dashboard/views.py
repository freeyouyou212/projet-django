from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect # Ajout de redirect
from django.contrib import messages # Ajout de messages
from django.utils import timezone
from apps.offers.models import Offer, Application

def superuser_required(user):
    """Vérifie que l'utilisateur est bien le Super Admin."""
    return user.is_superuser

@login_required
@user_passes_test(superuser_required, login_url='offers:offer_list')
def admin_dashboard(request):
    """
    Tableau de bord RÉSERVÉ à l'Administrateur (Superuser).
    L'enseignant (Staff) ne peut pas voir cette page.
    """
    offers_received = Offer.objects.count()
    offers_active = Offer.objects.filter(status="validated").count()
    applications_submitted = Application.objects.count()

    offers_by_status = (
        Offer.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    now = timezone.now()
    last_year = now - timedelta(days=365)

    applications_last_year = (
        Application.objects.filter(application_date__gte=last_year)
        .annotate(month=TruncMonth('application_date'))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    recent_offers = Offer.objects.order_by("-submission_date")[:10]

    context = {
        "offers_received": offers_received,
        "offers_active": offers_active,
        "applications_submitted": applications_submitted,
        "offers_by_status": list(offers_by_status),
        "applications_last_year": list(applications_last_year),
        "recent_offers": recent_offers,
    }
    return render(request, "dashboard/admin_dashboard.html", context)