from django.db import models

# Categorías para clasificar los cursos 🏷️
class Category(models.Model):
    name = models.CharField(max_length=100)      # Nombre visible (Ej: "Python", "Diseño") 📛
    slug = models.SlugField(unique=True)         # Versión URL-friendly (Ej: "python") 🔗

    def __str__(self):
        return self.name