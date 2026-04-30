from django.contrib import admin # Importamos el panel de administración de Django 🛠️
from .models import (Category, Course, CourseCategory,
                     Module, Enrollment, Progress, Review) # Traemos todos nuestros modelos (tablas) para usarlos aquí 📦

# --- CONFIGURACIÓN PARA CATEGORÍAS 🏷️ ---

@admin.register(Category) # Registramos el modelo Categoría en el panel  registre
class CategoryAdmin(admin.ModelAdmin): # Configuramos cómo se verá la Categoría ⚙️
    prepopulated_fields = {'slug': ('name',)} # El 'slug' se escribe solito mientras escribes el nombre ✍️⚡
    list_display = ('name', 'slug') # Columnas que se verán en la tabla principal 📋
    search_fields = ('name',) # Añadimos una barra de búsqueda para filtrar por nombre 🔍


# --- CONFIGURACIÓN PARA CURSOS 🎓 ---

@admin.register(Course) # Registramos el modelo Curso 📚
class CourseAdmin(admin.ModelAdmin): # Personalizamos el panel de Cursos 🛠️
    list_display = ['title', 'created_at'] # Queremos ver el título y la fecha de creación 📅
    list_filter = ['created_at'] # Filtro lateral para buscar por fecha rápidamente ⏳
    search_fields = ['title', 'overview'] # Buscador por título o descripción del curso 🔍
    prepopulated_fields = {'slug': ('title',)} # El slug se genera automáticamente usando el título 🪄


# --- CONFIGURACIÓN PARA RELACIÓN CURSO-CATEGORÍA 🔗 ---

@admin.register(CourseCategory) # Registramos la tabla intermedia de categorías 🤝
class CourseCategoryAdmin(admin.ModelAdmin): # Personalizamos su vista ⚙️
    list_display = ('course', 'category') # Mostramos qué curso pertenece a qué categoría 📑
    list_filter = ('category',) # Filtro lateral por categorías 🏷️
    search_fields = ('course__title',) # Buscador usando el título del curso relacionado 🔍


# --- CONFIGURACIÓN PARA MÓDULOS 🧩 ---

@admin.register(Module) # Registramos los Módulos de los cursos 🧱
class ModuleAdmin(admin.ModelAdmin): # Personalizamos la vista de Módulos 🛠️
    list_display = ('title', 'course') # Mostramos el título del módulo y a qué curso pertenece 📖
    list_filter = ('title', 'course__title') # Filtros por nombre de módulo o curso 🧐


# --- CONFIGURACIÓN PARA INSCRIPCIONES 📝 ---

@admin.register(Enrollment) # Registramos las Inscripciones de alumnos ✅
class EntollmentAdmin(admin.ModelAdmin): # Configuramos el panel de inscritos 👤
    list_display = ('user', 'course', 'enrolled_at') # Quién se inscribió, en qué curso y cuándo ⏰
    list_filter = ('course', 'enrolled_at') # Filtros por curso y fecha de inscripción 📊
    search_fields = ('user__username', 'course__title') # Buscar por nombre de usuario o curso 🔍


# --- CONFIGURACIÓN PARA PROGRESO 📈 ---

@admin.register(Progress) # Registramos el seguimiento del alumno 🏃‍♂️
class ProgressAdmin(admin.ModelAdmin): # Personalizamos la vista de progreso ⚙️
    list_display = ('user', 'course', 'progress', 'status', 'updated_at') # Mostramos porcentaje, estado y última vez 🏁
    list_filter = ('status',) # Filtro por estado (completado, en curso, etc.) 🚦
    search_fields = ('user__username', 'course__title') # Buscador por alumno o curso 🔍


# --- CONFIGURACIÓN PARA RESEÑAS ⭐ ---

@admin.register(Review) # Registramos las Opiniones de los cursos 💬
class ReviewAdmin(admin.ModelAdmin): # Personalizamos el panel de reseñas 🛠️
    list_display = ('user', 'course', 'rating', 'created_at') # Mostramos quién opinó, qué nota puso y cuándo 🌟
    list_filter = ('rating', 'created_at') # Filtros por estrellas y fecha 📅
    search_fields = ('user__username', 'course__title', 'comment') # Buscar por usuario, curso o el texto del comentario 🔍