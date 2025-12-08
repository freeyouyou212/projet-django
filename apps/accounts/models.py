from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

