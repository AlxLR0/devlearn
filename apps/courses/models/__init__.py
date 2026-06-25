# Exportamos todos los modelos del paquete courses/models/ 📦
# Así se pueden importar así: from apps.courses.models import Course, Module, etc.
from .category import Category                        # Categorías 🏷️
from .course import Course, CourseCategory            # Cursos y su tabla intermedia con categorías 📚
from .module import Module                            # Módulos de cada curso 🧩
from .enrollment import Enrollment                    # Inscripciones 📝
from .progress import Progress                        # Progreso general 📈
from .review import Review                            # Reseñas y calificaciones ⭐
from .content import Content, Text, Video, File, Image  # Contenidos (genérico + 4 tipos) 📦
from .progress_tracking import CompletedContent       # Contenido completado ✅