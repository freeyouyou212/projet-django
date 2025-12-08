from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "contact_email")
    search_fields = ("name", "contact_name", "contact_email")
