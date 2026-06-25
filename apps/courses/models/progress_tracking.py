from django.db import models
from django.conf import settings
from .content import Content  # Importamos Content (el contenido a marcar como visto) 📖

# Registro de contenido COMPLETADO por un usuario ✅
# Sirve para trackear QUÉ lecciones ha visto cada alumno
class CompletedContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)          # Alumno 👤
    content = models.ForeignKey(Content, on_delete=models.CASCADE)   # Contenido completado 📦
    completed_at = models.DateTimeField(auto_now_add=True)      # Cuándo lo terminó ⏰

    class Meta:
        unique_together = ('user', 'content')  # No se puede marcar 2 veces el mismo contenido 🚫
