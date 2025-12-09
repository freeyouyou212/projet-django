from django.test import TestCase
from .models import Offer

class OfferModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Offer.objects.create(
            organization="Test Organization",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            title="Test Internship",
            details="This is a test internship offer.",
            status="en attente validation"
        )

    def test_offer_content(self):
        offer = Offer.objects.get(id=1)
        expected_organization = f'{offer.organization}'
        expected_contact_name = f'{offer.contact_name}'
        expected_contact_email = f'{offer.contact_email}'
        expected_title = f'{offer.title}'
        expected_details = f'{offer.details}'
        expected_status = f'{offer.status}'

        self.assertEqual(expected_organization, "Test Organization")
        self.assertEqual(expected_contact_name, "John Doe")
        self.assertEqual(expected_contact_email, "john.doe@example.com")
        self.assertEqual(expected_title, "Test Internship")
        self.assertEqual(expected_details, "This is a test internship offer.")
        self.assertEqual(expected_status, "en attente validation")

class OfferViewTest(TestCase):

    def setUp(self):
        self.offer = Offer.objects.create(
            organization="Test Organization",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            title="Test Internship",
            details="This is a test internship offer.",
            status="en attente validation"
        )

    def test_offer_list_view(self):
        response = self.client.get('/offers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_list.html')

    def test_offer_detail_view(self):
        response = self.client.get(f'/offers/{self.offer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offers/offer_detail.html')

    def test_offer_create_view(self):
        response = self.client.post('/offers/create/', {
            'organization': 'New Organization',
            'contact_name': 'Jane Doe',
            'contact_email': 'jane.doe@example.com',
            'title': 'New Internship',
            'details': 'This is a new internship offer.',
            'status': 'en attente validation'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Offer.objects.filter(title='New Internship').exists())