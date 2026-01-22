from django.urls import path
from .views import lista_cursos, detalle_curso, cuestionario,feedback, calendario_view

urlpatterns = [
    path('', lista_cursos, name='lista_cursos'),
    path('<int:curso_id>/', detalle_curso, name='detalle_curso'),
    path('<int:curso_id>/cuestionario/', cuestionario, name='cuestionario'),
    path('<int:curso_id>/feedback/', feedback, name='feedback'),
    path('calendario/', calendario_view, name='calendario'),
]
