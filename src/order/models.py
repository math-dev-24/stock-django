from django.contrib.auth.models import User
from django.db import models
import uuid


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nom de la société")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    members = models.ManyToManyField(User, related_name="companies", verbose_name="Membres")

    def __str__(self):
        return self.name
