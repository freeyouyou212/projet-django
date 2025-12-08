from rest_framework import serializers
from apps.offers.models import InternshipOffer, Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'offer', 'student_name', 'student_email', 'application_date']
        read_only_fields = ['id', 'application_date']

class InternshipOfferSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = InternshipOffer
        fields = [
            'id',
            'organization',
            'contact_name',
            'contact_email',
            'submission_date',
            'title',
            'details',
            'status',
            'applications',
        ]
        read_only_fields = ['id', 'submission_date', 'applications']