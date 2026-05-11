from django.contrib import admin # Importamos el panel de control de Django 🛠️
from .models import (Category, Course, CourseCategory,
                     Module, Enrollment, Progress, Review, Content, Text, Video, File, Image) # Traemos todos nuestros modelos (tablas) para usarlos aquí 📦
# Register your models here.


@admin.register(Category) # Registramos las Categorías en el panel ✅
class CategoryAdmin(admin.ModelAdmin): # Configuramos cómo se verán las Categorías ⚙️
    prepopulated_fields = {'slug': ('name',)} # El slug se escribe solo mientras pones el nombre ✍️⚡
    list_display = ('name', 'slug') # Columnas que se verán en la lista principal 📋
    search_fields = ('name',) # Barra de búsqueda para encontrar por nombre 🔍


@admin.register(Course) # Registramos los Cursos 📚
class CourseAdmin(admin.ModelAdmin): # Personalizamos el panel de Cursos 🛠️
    list_display = ['title', 'created_at'] # Queremos ver el título y la fecha de creación 📅
    list_filter = ['created_at'] # Filtro lateral para buscar por fecha ⏳
    search_fields = ['title', 'overview'] # Buscador por título o descripción 🔍
    prepopulated_fields = {'slug': ('title',)} # El slug se genera solito con el título 🪄


@admin.register(CourseCategory) # Registramos la relación entre Cursos y Categorías 🔗
class CourseCategoryAdmin(admin.ModelAdmin): # Personalizamos su vista ⚙️
    list_display = ('course', 'category') # Mostramos qué curso está en qué categoría 📑
    list_filter = ('category',) # Filtro lateral para ver categorías específicas 🏷️
    search_fields = ('course__title',) # Buscador usando el nombre del curso 🔍


@admin.register(Module) # Registramos los Módulos (temas) de los cursos 🧩
class ModuleAdmin(admin.ModelAdmin): # Personalizamos la vista de Módulos 🛠️
    list_display = ('title', 'course') # Mostramos el título del tema y su curso 📖
    list_filter = ('title', 'course__title') # Filtros por nombre de tema o de curso 🧐


@admin.register(Enrollment) # Registramos las Inscripciones de los alumnos 📝
class EntollmentAdmin(admin.ModelAdmin): # Configuramos el panel de inscritos 👤
    list_display = ('user', 'course', 'enrolled_at') # Quién se inscribió, a qué y cuándo ⏰
    list_filter = ('course', 'enrolled_at') # Filtros por curso y fecha 📊
    search_fields = ('user__username', 'course__title') # Buscar por usuario o curso 🔍


@admin.register(Progress) # Registramos el Progreso de cada alumno 📈
class ProgressAdmin(admin.ModelAdmin): # Personalizamos la vista del progreso ⚙️
    list_display = ('user', 'course', 'progress', 'status', 'updated_at') # Mostramos porcentaje, estado y fecha 🏁
    list_filter = ('status',) # Filtro para ver quién terminó o sigue estudiando 🚦
    search_fields = ('user__username', 'course__title') # Buscador por alumno o curso 🔍


@admin.register(Review) # Registramos las Reseñas y estrellas ⭐
class ReviewAdmin(admin.ModelAdmin): # Personalizamos el panel de opiniones 🛠️
    list_display = ('user', 'course', 'rating', 'created_at') # Quién opinó, cuántas estrellas y cuándo 🌟
    list_filter = ('rating', 'created_at') # Filtros por nota y fecha 📅
    search_fields = ('user__username', 'course__title', 'comment') # Buscar por usuario, curso o texto 💬


@admin.register(Content) # Registramos el Contenido general de los módulos 📦
class ContentAdmin(admin.ModelAdmin): # Personalizamos la vista de contenidos ⚙️
    list_display = ('module', 'content_type', 'item') # Mostramos el módulo, el tipo y el objeto real 📑
    list_filter = ('module',) # Filtro para ver contenidos de un módulo específico 📂


@admin.register(Text) # Registramos los contenidos de Texto 📝
class TextAdmin(admin.ModelAdmin): # Panel para los textos 🛠️
    list_display = ('owner', 'title', 'updated_at', 'content') # Dueño, título, fecha y el texto ✍️


@admin.register(File) # Registramos los Archivos descargables 📁
class FileAdmin(admin.ModelAdmin): # Panel para los archivos ⚙️
    list_display = ('owner', 'title', 'updated_at', 'file') # Dueño, título, fecha y el archivo 📎


@admin.register(Video) # Registramos los Videos de las lecciones 🎥
class VideoAdmin(admin.ModelAdmin): # Panel para los videos 🛠️
    list_display = ('owner', 'title', 'updated_at', 'url') # Dueño, título, fecha y link del video 🔗


@admin.register(Image) # Registramos las Imágenes 🖼️
class ImageAdmin(admin.ModelAdmin): # Panel para las imágenes ⚙️
    list_display = ('owner', 'title', 'updated_at', 'file') # Dueño, título, fecha y la imagen 📷