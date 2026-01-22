from django.contrib import admin
from .models import (
    Curso,
    ProgresoCurso,
    Pregunta,
    Opcion,
    ResultadoCuestionario,
    Feedback,
    Evento
)


admin.site.register(Curso)
admin.site.register(ProgresoCurso)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(ResultadoCuestionario)
admin.site.register(Feedback)
admin.site.register(Evento)