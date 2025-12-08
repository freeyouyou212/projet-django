from datetime import timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from apps.offers.models import Offer, Application


def staff_required(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(staff_required)
def admin_dashboard(request):
    """
    Tableau de bord admin :
    - nb total d'offres
    - nb d'offres actives (validées)
    - nb total de candidatures
    - répartition par statut
    - candidatures par mois sur 12 mois
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
        .extra(select={"month": "strftime('%%m', application_date)"})
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    recent_offers = Offer.objects.order_by("-submission_date")[:10]

    context = {
        "offers_received": offers_received,
        "offers_active": offers_active,
        "applications_submitted": applications_submitted,
        "offers_by_status": offers_by_status,
        "applications_last_year": applications_last_year,
        "recent_offers": recent_offers,
    }
    return render(request, "dashboard/admin_dashboard.html", context)
