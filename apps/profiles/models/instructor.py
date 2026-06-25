from django.db import models
from django.conf import settings

# Perfil extra para los instructores 🧑‍🏫
# Se crea automáticamente cuando un usuario es marcado como instructor (ver signals.py)
class InstructorProfile(models.Model):
    # Relación 1 a 1 con el User (cada instructor tiene UN perfil) 🔗
    # related_name='instructor_profile' permite acceder desde User: user.instructor_profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True)                  # Biografía del instructor 📝
    photo = models.URLField(blank=True, null=True)      # Foto de perfil (URL externa) 🖼️
    website = models.URLField(blank=True, null=True)    # Sitio web personal 🌐
    linkedin_url = models.URLField(blank=True, null=True)  # LinkedIn 🔗
    social_network = models.URLField(blank=True, null=True) # Otra red social 📱

    def __str__(self):
        return f"Instructor: {self.user.get_full_name() or self.user.username}"
