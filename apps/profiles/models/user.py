# Importamos AbstractUser de Django para personalizar el usuario base 👤
from django.contrib.auth.models import AbstractUser
from django.db import models

# Nuestro modelo de Usuario personalizado ⚡
# Reemplaza al User de Django por defecto (configurado en settings.py con AUTH_USER_MODEL)
class User(AbstractUser):
    # Campo extra: indica si el usuario es instructor o no 🧑‍🏫
    # Los instructores pueden crear cursos, los estudiantes solo consumirlos
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        # Mostramos el nombre completo si existe, sino el username
        return self.get_full_name() or self.username
