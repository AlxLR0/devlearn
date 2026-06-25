from django.db import models
from django.conf import settings
from .course import Course  # Importamos Course 📚

# Progreso de un usuario en un curso 📈
# Se actualiza automáticamente cada vez que el alumno completa contenido
class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Alumno 👤
    course = models.ForeignKey(Course, on_delete=models.CASCADE)                  # Curso 📚
    status = models.CharField(max_length=50)            # Estado: "en_progreso", "completado", etc. 🚦
    updated_at = models.DateTimeField(auto_now=True)    # Última vez que se actualizó 🔄
    progress = models.FloatField(default=0.0)           # Porcentaje de avance (0.0 a 100.0) 📊

    class Meta:
        unique_together = ('user', 'course')  # Un solo progreso por usuario+curso 🎯

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'