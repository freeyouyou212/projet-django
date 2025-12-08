from django.db import models
from django.utils import timezone

class InternshipOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente de validation'),
        ('validated', 'Validée'),
        ('rejected', 'Refusée'),
        ('closed', 'Clôturée'),
    ]

    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    details = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    submission_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} — {self.organization}"

    @property
    def applications_count(self) -> int:
        """Nombre de candidatures déjà reçues."""
        return self.applications.count()

    @property
    def is_open_for_applications(self) -> bool:
        """
        Offre encore ouverte aux candidatures ?
        Règle métier : statut VALIDATED et moins de 5 candidatures.
        """
        return self.status == 'validated' and self.applications_count < 5


class Application(models.Model):
    """Candidature à une offre de stage."""
    offer = models.ForeignKey(
        InternshipOffer,
        related_name='applications',
        on_delete=models.CASCADE,
    )
    student_name = models.CharField(max_length=255)
    student_email = models.EmailField()
    application_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-application_date"]
        # Un même étudiant (email) ne peut pas candidater 2 fois à la même offre
        unique_together = ("offer", "student_email")

    def __str__(self) -> str:
        return f"{self.student_name} → {self.offer.title}"

# Alias pour compatibilité
Offer = InternshipOffer