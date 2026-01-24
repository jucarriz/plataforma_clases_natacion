from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.contrib.auth import views as auth_views
from .models import Perfil
from django.contrib.auth.models import User

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {}
        username = request.GET.get('username')
        if username:
            initial_data['username'] = username

        form = RegistroForm(initial=initial_data)

    return render(request, 'registro.html', {
        'form': form,
        'layout': 'layout-auth'
    })

def login_usuario(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        username = request.POST.get('username')

        # 🔍 Si el usuario NO existe → redirigir a registro
        if username and not User.objects.filter(username=username).exists():
            return redirect(f"/registro/?username={username}")

        # Si existe, intentamos login normal
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Usuario o contraseña incorrectos."

    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'error': error,
        'layout': 'layout-auth'
    })


@login_required
def dashboard(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {
        'perfil': perfil,
        'layout': 'layout-dashboard'
    })



def logout_usuario(request):
    logout(request)
    return redirect('login')

from django.contrib.auth import views as auth_views


class PasswordResetViewCustom(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layout'] = 'layout-auth'
        return context


class PasswordResetDoneViewCustom(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layout'] = 'layout-auth'
        return context


class PasswordResetConfirmViewCustom(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layout'] = 'layout-auth'
        return context


class PasswordResetCompleteViewCustom(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['layout'] = 'layout-auth'
        return context
