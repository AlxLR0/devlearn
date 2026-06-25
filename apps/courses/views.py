# ⚠️ NOTA: Este archivo ya NO se usa activamente.
# Las vistas ahora están divididas en views/instructor.py y views/student.py
# Se mantiene por referencia / compatibilidad (versión anterior del código).

from django.shortcuts import render, get_object_or_404
from .models.course import Course        # Modelo Course (models/course.py) 📚
from .models.progress import Progress    # Modelo Progress (models/progress.py) 📈
from django.db.models import Q
from django.core.paginator import Paginator


def course_list(request):
    # Listado de cursos con búsqueda y paginación 🔍
    courses = Course.objects.all()
    query = request.GET.get("q")

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(owner__first_name__icontains=query)
        )

    paginator = Paginator(courses, 8)
    page_number = request.GET.get("page")
    courses_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    query_string = query_params.urlencode()

    return render(request, "courses/courses.html", {
        'courses_obj': courses_obj,
        'query': query,
        'query_string': query_string
    })


def course_detail(request, slug):
    # ── Detalle de un curso (versión legacy, sin reseñas ni inscripción) ──
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('contents')
    total_contents = sum(module.contents.count() for module in modules)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'total_contents': total_contents
    })


def course_lessons(request, slug):
    # ── Lecciones (versión legacy, sin tracking detallado por contenido) ──
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('contents')

    # ── Intentamos obtener el progreso guardado ──
    course_progress = 0  # Por defecto, progreso 0%
    # ── Evaluamos si el usuario está logueado ──
    if request.user.is_authenticated:
        # ✅ Sí -> buscamos su progreso en este curso
        progress_obj = Progress.objects.filter(
            user=request.user, course=course).first()
        # ── Evaluamos si existe un registro de progreso ──
        if progress_obj:
            # ✅ Sí -> usamos ese valor
            course_progress = progress_obj.progress
        # ❌ Si no existe progreso, se queda en 0
    # ❌ Si no está logueado, se queda en 0 (no mostramos progreso)

    return render(request, 'courses/course_lessons.html', {
        'course_title': course.title,
        'modules': modules,
        'course_progress': course_progress  # 📊 Se envía al template para mostrarlo
    })