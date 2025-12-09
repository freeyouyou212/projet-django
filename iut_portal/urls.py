from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),        
    path('accounts/', include('django.contrib.auth.urls')),   
    path('dashboard/', include('dashboard.urls')),       
    path('', include('offers.urls')),                   
]
