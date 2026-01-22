from django.urls import path
from .views import registro, login_usuario, dashboard, logout_usuario

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', login_usuario, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_usuario, name='logout'),
]
