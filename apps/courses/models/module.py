
from django.db import models
from .course import Course  # FK al curso al que pertenece el módulo 📚
from ..fields import OrderField  # Campo personalizado que auto-asigna el orden 🎯


# Cada curso tiene varios MÓDULOS (como "capítulos" o "unidades") 🧩
class Module(models.Model):
    # FK al curso dueño del módulo 🔗
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='modules')

    title = models.CharField(max_length=200)        # Título del módulo 📛
    description = models.TextField(blank=True)      # Descripción (opcional) 📝
    # Orden automático: se asigna solo basado en otros módulos del mismo curso 🔢
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f"{self.course.title} - {self.title}"