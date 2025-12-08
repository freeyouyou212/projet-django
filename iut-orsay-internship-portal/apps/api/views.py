from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from apps.offers.models import InternshipOffer, Application
from .serializers import InternshipOfferSerializer, ApplicationSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = InternshipOffer.objects.all().order_by('-submission_date')
    serializer_class = InternshipOfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-application_date')
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]