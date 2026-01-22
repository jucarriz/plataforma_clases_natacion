from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(unique=True)
    archivo_video = models.CharField(
    max_length=100,
    default='video1.txt',
    help_text="Nombre del archivo .txt del video (ej: video1.txt)")

    def __str__(self):
        return f"Curso {self.orden} - {self.titulo}"

from django.contrib.auth.models import User

class ProgresoCurso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"{self.usuario.email} - {self.curso} - {'OK' if self.completado else 'Pendiente'}"
    
class Pregunta(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=300)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto


class ResultadoCuestionario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    correctas = models.PositiveIntegerField()
    incorrectas = models.PositiveIntegerField()
    aprobado = models.BooleanField()

    def __str__(self):
        return f"{self.usuario.email} - {self.curso}"

class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')

    def __str__(self):
        return f"Feedback de {self.usuario.email} - {self.curso}"


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

