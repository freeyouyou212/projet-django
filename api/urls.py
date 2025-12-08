from django.urls import path, include
from rest_framework import routers
from .views import OfferViewSet, ApplicationViewSet

router = routers.DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]