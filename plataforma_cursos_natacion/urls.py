from django.contrib import admin
from django.urls import path, include
from usuarios.views import (
    PasswordResetViewCustom,
    PasswordResetDoneViewCustom,
    PasswordResetConfirmViewCustom,
    PasswordResetCompleteViewCustom,
)
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', home_redirect),
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('cursos/', include('cursos.urls')),

    # 🔐 Recuperar contraseña (SOLO custom)
    path('password-reset/', PasswordResetViewCustom.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneViewCustom.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmViewCustom.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteViewCustom.as_view(), name='password_reset_complete'),
]
