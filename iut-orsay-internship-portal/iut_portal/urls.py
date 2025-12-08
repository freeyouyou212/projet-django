from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),         # signup + dashboard
    path('accounts/', include('django.contrib.auth.urls')),   # login/logout/password reset
    path('dashboard/', include('apps.dashboard.urls')),       # <-- AJOUT
    path('', include('apps.offers.urls')),                    # home -> offers
]
