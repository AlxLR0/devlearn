from django.db import models
from django.conf import settings
from .course import Course  # Importamos el modelo Course 📚

# Inscripción de un usuario a un curso 📝
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Alumno 👤
    course = models.ForeignKey(Course, on_delete=models.CASCADE)                  # Curso 📚
    enrolled_at = models.DateTimeField(auto_now_add=True)                         # Fecha de inscripción 📅

    class Meta:
        unique_together = ('user', 'course')  # Un usuario solo puede inscribirse UNA vez al mismo curso ⛔

    def __str__(self):
        return f'{self.user.username} inscrito en {self.course.title}'