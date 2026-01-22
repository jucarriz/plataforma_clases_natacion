from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso_actual = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Perfil de {self.user.email}"
