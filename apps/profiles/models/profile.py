from django.db import models
from .user import User  # Importamos nuestro User personalizado (vive en el mismo paquete models/) 👤

# Perfil general de TODOS los usuarios (tanto estudiantes como instructores) 🧑‍🎓
# Se crea automáticamente al registrarse (ver signals.py)
class Profile(models.Model):
    # Relación 1 a 1 con User (cada usuario tiene UN perfil) 🔗
    # related_name='profile' permite acceder desde User: user.profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=255, blank=True)       # Empresa donde trabaja 🏢
    profession = models.CharField(max_length=255, blank=True)    # Profesión 💼
    timezone = models.CharField(max_length=255, blank=True)      # Zona horaria 🌐
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  # Foto de perfil (archivo subido) 🖼️

    def __str__(self):
        return f'Profile for {self.user.username}'
