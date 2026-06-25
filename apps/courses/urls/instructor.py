# URLs del lado INSTRUCTOR 👨‍🏫
# Todas estas rutas empiezan con /instructor/ (configurado en devlearn/urls.py)
from django.urls import path
from django.views.generic import RedirectView
from ..views import instructor  # Vistas del instructor (viven en views/instructor.py) 🎯

app_name = 'instructor'

urlpatterns = [
    # Redirige /instructor/ a /instructor/courses/ automáticamente 🔄
    path('', RedirectView.as_view(pattern_name='instructor:course_list', permanent=True)),

    # --- CRUD de Cursos 📚 ---
    path('courses/', instructor.CourseListView.as_view(), name="course_list"),          # Listar cursos
    path('course/create', instructor.CourseCreateView.as_view(), name="course_create"), # Crear curso
    path('course/<int:pk>/edit/', instructor.CourseUpdateView.as_view(), name="course_edit"),   # Editar
    path('course/<int:pk>/delete/', instructor.CourseDeleteView.as_view(), name="course_delete"), # Eliminar

    # --- CRUD de Módulos 🧩 ---
    path('course/<int:course_id>/modules/', instructor.ModuleListView.as_view(), name='module_list'),    # Listar módulos
    path('course/<int:course_id>/modules/add', instructor.ModuleCreateView.as_view(), name='module_add'),# Crear módulo
    path('modules/<int:pk>/edit/', instructor.ModuleUpdateView.as_view(), name='module_edit'),           # Editar
    path('module/<int:pk>/delete/', instructor.ModuleDeleteView.as_view(), name='module_delete'),        # Eliminar

    # --- CRUD de Contenidos 📦 ---
    path('module/<int:module_id>/contents/', instructor.ContentListView.as_view(), name='content_list'), # Listar contenidos
    # <model_name> puede ser 'text', 'video', 'image' o 'file'
    path('module/<int:module_id>/content/<model_name>/add/', instructor.ContentCreateUpdateView.as_view(), name="content_add"),   # Crear
    path('module/<int:module_id>/content/<int:id>/<model_name>/edit/', instructor.ContentCreateUpdateView.as_view(), name="content_edit"), # Editar
    path('content/<int:pk>/delete/', instructor.ContentDeleteView.as_view(), name='content_delete'),     # Eliminar

    # --- Reordenamiento (drag & drop) 🔄 ---
    path('module/order/', instructor.ModuleOrderView.as_view(), name="module_order"),    # Reordenar módulos
    path('content/order/', instructor.ContentOrderView.as_view(), name="content_order")  # Reordenar contenidos
]