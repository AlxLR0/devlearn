# URLs del lado ESTUDIANTE 🧑‍🎓
# Todas estas rutas empiezan con /student/ (configurado en devlearn/urls.py)
from django.urls import path
from django.views.generic import RedirectView
from ..views import student  # Vistas del estudiante (viven en views/student.py) 🎯

app_name = 'student'

urlpatterns = [
    # Redirige /student/ a /student/courses/ automáticamente 🔄
    path('', RedirectView.as_view(pattern_name='student:course_list', permanent=True)),

    path("courses/", student.course_list, name="course_list"),          # Listado de cursos 📋
    path("detail/<str:slug>", student.course_detail, name="course_detail"),  # Detalle de un curso 📖
    # Página de lecciones (con o sin content_id específico) 📚
    path("<str:slug>/lessons/<int:content_id>/", student.course_lessons, name="course_lessons"),
    path("<str:slug>/lessons/", student.course_lessons, name="course_lessons"),
    # Marcar contenido como completado ✅
    path('content/<int:content_id>/complete/', student.mark_complete, name="mark_complete"),
    # Dejar/editar reseña de un curso ⭐
    path("<str:slug>/review/", student.review_course, name="review_course")
]