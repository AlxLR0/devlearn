from django.db import models
from django.conf import settings
from .category import Category  # Importamos Category para la relación ManyToMany 🏷️

# Modelo principal: un CURSO 📚
class Course(models.Model):
    # Dueño del curso (instructor que lo creó) - FK al modelo User (profiles/models/user.py) 👨‍🏫
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_courses')
    title = models.CharField(max_length=200)        # Título del curso 📛
    slug = models.SlugField(unique=True)            # Slug único para URLs amigables 🔗
    overview = models.TextField()                   # Descripción general del curso 📝
    created_at = models.DateField(auto_now_add=True) # Fecha de creación (automática) 📅
    # Relación M:M con Category a través de CourseCategory (tabla intermedia) 🔗
    categories = models.ManyToManyField(
        Category, through='CourseCategory', related_name='courses')
    image = models.URLField()                       # URL de la imagen de portada 🖼️
    level = models.CharField(max_length=50)         # Nivel: Principiante, Intermedio, Avanzado 📊
    rating = models.FloatField(default=0.0)         # Calificación promedio (se calcula de las reviews) ⭐
    duration = models.FloatField(default=0.0)       # Duración estimada en horas ⏱️

    class Meta:
        ordering = ['-created_at']  # Los más nuevos primero ⬇️

    def __str__(self):
        return self.title

# Tabla intermedia para la relación ManyToMany entre Course y Category 🔗
class CourseCategory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'category')  # Un curso no puede tener la misma categoría repetida ⛔

    def __str__(self):
        return f"{self.course} - {self.category}"