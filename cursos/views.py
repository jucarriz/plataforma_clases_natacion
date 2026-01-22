import os
from django.conf import settings
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    Curso,
    ProgresoCurso,
    Pregunta,
    Opcion,
    ResultadoCuestionario
)
from .models import Feedback, Evento
from .forms import FeedbackForm
import calendar

@login_required
def lista_cursos(request):
    cursos = Curso.objects.order_by('orden')
    progreso = ProgresoCurso.objects.filter(usuario=request.user)

    cursos_disponibles = []

    for curso in cursos:
        if curso.orden == 1:
            disponible = True
        else:
            curso_anterior = Curso.objects.get(orden=curso.orden - 1)
            disponible = progreso.filter(
                curso=curso_anterior,
                completado=True
            ).exists()

        cursos_disponibles.append({
            'curso': curso,
            'disponible': disponible
        })

    return render(request, 'cursos/lista_cursos.html', {
    'cursos_disponibles': cursos_disponibles,
    'layout': 'layout-cursos'
    })



@login_required
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Curso anterior
    curso_anterior = Curso.objects.filter(orden=curso.orden - 1).first()

    # Si NO es el primer curso, verificar progreso del anterior
    if curso_anterior:
        progreso_anterior = ProgresoCurso.objects.filter(
            usuario=request.user,
            curso=curso_anterior,
            completado=True
        ).exists()

        if not progreso_anterior:
            return redirect('lista_cursos')

    # Obtener o crear progreso del curso actual
    progreso, _ = ProgresoCurso.objects.get_or_create(
        usuario=request.user,
        curso=curso
    )

    # Leer video (lo que ya tenías)
    import os
    from django.conf import settings

    ruta_video = os.path.join(
        settings.BASE_DIR,
        'videos',
        curso.archivo_video
    )

    video_url = None
    if os.path.exists(ruta_video):
        with open(ruta_video, 'r', encoding='utf-8') as f:
            video_url = f.read().strip()

    # Marcar curso como completado
    if request.method == 'POST':
        progreso.completado = True
        progreso.save()
        return redirect('lista_cursos')

    return render(request, 'cursos/detalle_curso.html', {
    'curso': curso,
    'video_url': video_url,
    'progreso': progreso,
    'layout': 'layout-dashboard'   # 👈 CAMBIO CLAVE
})

@login_required
def cuestionario(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Obtener preguntas del curso
    preguntas = Pregunta.objects.filter(curso=curso)

    # Si no hay preguntas, volver a cursos
    if not preguntas.exists():
        return redirect('lista_cursos')

    if request.method == 'POST':
        correctas = 0
        incorrectas = 0

        for pregunta in preguntas:
            opcion_id = request.POST.get(str(pregunta.id))
            if opcion_id:
                opcion = Opcion.objects.get(id=opcion_id)
                if opcion.es_correcta:
                    correctas += 1
                else:
                    incorrectas += 1

        total = preguntas.count()
        aprobado = correctas >= (total * 0.7)  # 70% mínimo

        ResultadoCuestionario.objects.create(
            usuario=request.user,
            curso=curso,
            correctas=correctas,
            incorrectas=incorrectas,
            aprobado=aprobado
        )

        # Si aprueba, marcar curso como completado
        if aprobado:
            progreso, _ = ProgresoCurso.objects.get_or_create(
                usuario=request.user,
                curso=curso
            )
            progreso.completado = True
            progreso.save()

        return render(request, 'cursos/resultado.html', {
            'curso': curso,
            'correctas': correctas,
            'incorrectas': incorrectas,
            'aprobado': aprobado
        })

    return render(request, 'cursos/cuestionario.html', {
    'curso': curso,
    'preguntas': preguntas,
    'layout': 'layout-dashboard'
    })


@login_required
def feedback(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Evitar feedback duplicado
    if Feedback.objects.filter(usuario=request.user, curso=curso).exists():
        return redirect('lista_cursos')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.usuario = request.user
            feedback.curso = curso
            feedback.save()
            return redirect('lista_cursos')
    else:
        form = FeedbackForm()

    return render(request, 'cursos/feedback.html', {
    'curso': curso,
    'form': form,
    'layout': 'layout-dashboard'
})


@login_required
def calendario_view(request):
    hoy = date.today()

    year = int(request.GET.get('year', hoy.year))
    month = int(request.GET.get('month', hoy.month))

    cal = calendar.Calendar(firstweekday=0)  # Lunes
    dias_mes = list(cal.itermonthdates(year, month))

    eventos = Evento.objects.filter(
        fecha__year=year,
        fecha__month=month
    )

    eventos_por_dia = {}
    for evento in eventos:
        eventos_por_dia.setdefault(evento.fecha, []).append(evento)

    calendario = []
    for dia in dias_mes:
        if dia == hoy:
            color = '#d1ecf1'      # Hoy
        elif dia.month != month:
            color = '#f0f0f0'      # Otro mes
        else:
            color = 'white'        # Mes actual

        calendario.append({
            'fecha': dia,
            'eventos': eventos_por_dia.get(dia, []),
            'color': color
        })

    # Mes anterior
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    # Mes siguiente
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    return render(request, 'cursos/calendario.html', {
    'calendario': calendario,
    'mes': calendar.month_name[month],
    'anio': year,
    'prev_month': prev_month,
    'prev_year': prev_year,
    'next_month': next_month,
    'next_year': next_year,
    'layout': 'layout-dashboard'
})

