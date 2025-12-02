from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Ruta para registrarse (usa nuestra vista personalizada)
    path('registro/', views.registro, name='registro'),

    # Rutas para Login y Logout (usamos las clases genéricas de Django)
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]