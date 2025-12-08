from django.contrib import admin
from .models import InternshipOffer, Application


@admin.register(InternshipOffer)
class InternshipOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "status", "submission_date")
    list_filter = ("status", "organization")
    search_fields = ("title", "organization", "contact_name", "contact_email")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_email", "offer", "application_date")
    search_fields = ("student_name", "student_email", "offer__title")
