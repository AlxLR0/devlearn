from django.db import models
from django.conf import settings
from .course import Course  # Importamos Course 📚

# Reseña / calificación de un curso por parte de un alumno ⭐
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Alumno 👤
    course = models.ForeignKey(Course, on_delete=models.CASCADE)                  # Curso 📚
    rating = models.PositiveSmallIntegerField()         # Calificación (1 a 5 estrellas) ⭐
    comment = models.TextField(blank=True)              # Comentario opcional 💬
    created_at = models.DateTimeField(auto_now_add=True) # Fecha de la reseña 📅

    class Meta:
        unique_together = ('user', 'course')  # Un usuario solo deja UNA reseña por curso 🎯

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'