# ─────────────────────────────────────────────
# 🧑‍🎓 VISTAS DEL ESTUDIANTE
# ─────────────────────────────────────────────
# Aquí vive toda la lógica para que los alumnos:
# - Vean el catálogo de cursos 📋
# - Vean detalle de un curso 📖
# - Tomen lecciones y vean su progreso 📚
# - Marquen contenido como completado ✅
# - Dejen reseñas y calificaciones ⭐

from django.shortcuts import render, get_object_or_404, redirect
from ..models.course import Course           # Modelo Course (vive en models/course.py) 📚
from ..models.enrollment import Enrollment   # Inscripciones (models/enrollment.py) 📝
from ..models.progress_tracking import CompletedContent  # Contenido completado (models/progress_tracking.py) ✅
from ..models.content import Content         # Contenido genérico (models/content.py) 📦
from ..models.progress import Progress       # Progreso (models/progress.py) 📈
from ..models.review import Review           # Reseñas (models/review.py) ⭐
from django.db.models import Q               # Para búsquedas con OR/AND condicional 🔍
from django.core.paginator import Paginator  # Paginación (divide en páginas) 📄
from django.contrib.auth.decorators import login_required  # 🔒 Si no hay sesión, redirige a login
from django.contrib import messages           # Mensajes flash (notificaciones tipo toast) 💬
from ..forms import ReviewForm               # Formulario de reseñas (vive en forms.py) 📝
from django.db.models import Avg, Count     # Funciones de agregación para stats 📊


# ═══════════════════════════════════════════════
# 📋 LISTADO DE CURSOS (con filtros y búsqueda)
# ═══════════════════════════════════════════════
@login_required
def course_list(request):
    # ── Obtenemos parámetros de la URL ──
    query = request.GET.get("q")                # Búsqueda por texto 🔍
    filter_type = request.GET.get('filter', 'all')  # Filtro: 'all', 'enrolled', 'not_enrolled'
    # 💡 Si no hay ?filter=, por defecto 'all' (todos los cursos)

    # ── Filtramos según el tipo seleccionado ──
    if filter_type == 'enrolled':
        # 🟢 Solo cursos donde el usuario está inscrito
        courses = Course.objects.filter(enrollment__user=request.user)
    elif filter_type == 'not_enrolled':
        # 🔴 Solo cursos donde NO está inscrito
        courses = Course.objects.exclude(enrollment__user=request.user)
    else:
        # 🔵 Todos los cursos (sin filtro)
        courses = Course.objects.all()

    # ── Si hay texto de búsqueda, filtramos por título o instructor ──
    if query:
        # Q permite hacer OR entre condiciones
        # icontains: busca sin importar mayúsculas/minúsculas
        courses = courses.filter(
            Q(title__icontains=query) |           # 🎯 Coincide con el título
            Q(owner__first_name__icontains=query)  # 🎯 Coincide con el nombre del instructor
        )

    # ── Paginación: dividimos los resultados en páginas de 8 ──
    paginator = Paginator(courses, 8)
    page_number = request.GET.get("page")  # ¿En qué página estamos?
    courses_obj = paginator.get_page(page_number)  # Obtenemos los cursos de esta página

    # ── Preservamos los filtros al navegar entre páginas ──
    # Si no hacemos esto, al cambiar de página se pierde el ?filter=xxx
    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")  # Quitamos 'page' para no duplicarlo
    query_string = query_params.urlencode()  # Ej: "filter=enrolled&q=python"

    # ── Renderizamos el template con todos los datos ──
    return render(request, "courses/courses.html", {
        'courses_obj': courses_obj,      # 📦 Los cursos de la página actual
        'query': query,                   # 🔍 Texto buscado (para mantenerlo en el input)
        'query_string': query_string,     # 🔗 Filtros serializados (para links de paginación)
        'filter_type': filter_type        # 🏷️ Filtro activo (para resaltar el botón)
    })


# ═══════════════════════════════════════════════
# 📖 DETALLE DE UN CURSO
# ═══════════════════════════════════════════════
@login_required
def course_detail(request, slug):
    # ── Buscamos el curso por slug (URL amigable) ──
    # get_object_or_404: si no existe, lanza error 404
    course = get_object_or_404(Course, slug=slug)

    # Cargamos todos los módulos con sus contenidos (prefetch para optimizar) ⚡
    modules = course.modules.prefetch_related('contents').order_by('order')

    # ── Verificamos si el usuario YA está inscrito ──
    # .exists() es más eficiente que .count() o cargar el objeto
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    # ── Traemos las reseñas del curso (con datos del usuario para mostrar el nombre) ⭐ ──
    reviews = Review.objects.filter(course=course).select_related('user').order_by('-created_at')

    # ── Calculamos estadísticas de las reseñas ──
    # aggregate: hace cálculos en la DB (no en Python)
    stats = reviews.aggregate(
        avg=Avg('rating'),   # ⭐ Promedio de estrellas
        total=Count('id')    # 🔢 Cantidad de reseñas
    )
    # 💡 stats será algo como: {'avg': 4.5, 'total': 12}

    # ── Contamos el total de contenidos del curso (sumando los de cada módulo) ──
    total_contents = sum(module.contents.count() for module in modules)

    # ── Renderizamos ──
    return render(request, 'courses/course_detail.html', {
        'course': course,              # 📚 El curso
        'modules': modules,            # 🧩 Módulos con sus contenidos
        'total_contents': total_contents,  # 🔢 Total de lecciones
        'is_enrolled': is_enrolled,    # ✅ ¿Ya está inscrito?
        'reviews': reviews,            # ⭐ Lista de reseñas
        'stats': stats                 # 📊 {avg, total} de reseñas
    })


# ═══════════════════════════════════════════════
# 📚 PÁGINA DE APRENDIZAJE (lecciones + progreso)
# ═══════════════════════════════════════════════
@login_required
def course_lessons(request, slug, content_id=None):
    # ── Buscamos el curso y sus módulos ──
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('contents').order_by('order')

    # ── Guardamos el curso actual en la SESIÓN (para el dashboard) 🏠 ──
    # El dashboard usa estos datos para mostrar "seguir estudiando"
    request.session['last_course_slug'] = course.slug
    request.session['last_course_title'] = course.title
    request.session['last_course_image'] = course.image
    request.session.modified = True  # 🔄 Obliga a Django a guardar la sesión

    # ── AUTO-INSCRIPCIÓN: si entra a las lecciones, se inscribe automáticamente 📝 ──
    # get_or_create: si ya está inscrito, no hace nada
    Enrollment.objects.get_or_create(user=request.user, course=course)

    # ── Aplanamos todos los contenidos del curso en una sola lista ──
    # [contenido1, contenido2, ..., contenidoN] sin importar de qué módulo sean
    all_contents = [c for m in modules for c in m.contents.all()]
    total_contents = len(all_contents)  # Total de lecciones en el curso

    # ── Buscamos qué contenidos el usuario ya completó ✅ ──
    # values_list('content_id', flat=True) -> devuelve [id1, id2, id3, ...]
    completed = CompletedContent.objects.filter(
        user=request.user, content__in=all_contents
    ).values_list('content_id', flat=True)

    # ── Calculamos progreso POR MÓDULO (para mostrarlo en la interfaz) ──
    for module in modules:
        # ¿Cuántos contenidos de este módulo ha completado el usuario?
        module.completed_count = module.contents.filter(id__in=completed).count()
        # ¿Cuántos contenidos tiene este módulo en total?
        module.total_count = module.contents.count()
        # 💡 En el template: {{ module.completed_count }}/{{ module.total_count }}

    # ── Determinamos el contenido ACTUAL (el que está viendo el usuario) ──
    current_content = None
    if content_id:
        # Si hay un content_id en la URL, es el contenido que estamos viendo
        current_content = get_object_or_404(
            Content, id=content_id, module__course=course)

    # ── Calculamos el progreso TOTAL en porcentaje 📈 ──
    # (completados / total * 100), si no hay contenidos, progreso = 0
    if total_contents:
        progress = (len(completed) / total_contents * 100)
    else:
        progress = 0

    # ── Guardamos (o actualizamos) el progreso en la DB 💾 ──
    # update_or_create: si ya existe un Progress para este usuario+curso, lo actualiza
    # si no existe, lo crea
    Progress.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={'progress': progress}  # 'progress' es el % de avance
    )

    # ── Renderizamos ──
    return render(request, 'courses/course_lessons.html', {
        'course': course,               # 📚 El curso
        'modules': modules,             # 🧩 Módulos con progreso incluido
        'completed_ids': set(completed),  # ✅ Set de IDs completados (para marcar checkboxes)
        'current_content': current_content,  # 👀 Contenido actual (None si es la primera vez)
        'progress': int(progress)       # 📊 Progreso total como entero (0-100)
    })


# ═══════════════════════════════════════════════
# ✅ MARCAR CONTENIDO COMO COMPLETADO
# ═══════════════════════════════════════════════
@login_required
def mark_complete(request, content_id):
    # ── Buscamos el contenido que se quiere marcar ──
    content = get_object_or_404(Content, id=content_id)

    # ── Creamos el registro "contenido completado" (si ya existe, no hace nada) ──
    CompletedContent.objects.get_or_create(user=request.user, content=content)

    # ── Buscamos el SIGUIENTE contenido en el mismo módulo ──
    # Filtramos: mismo módulo, orden MAYOR al actual, ordenado ascendentemente
    next_content = Content.objects.filter(
        module=content.module,    # Mismo módulo
        order__gt=content.order   # Orden mayor al que acabo de completar
    ).order_by('order').first()   # El primero = el siguiente

    # ── Evaluamos si hay siguiente contenido ──
    if next_content:
        # ✅ Sí hay más -> redirigimos a la lección siguiente, pasando su ID
        return redirect('student:course_lessons',
                        slug=content.module.course.slug,
                        content_id=next_content.id)
        # 💡 Esto hará que course_lessons() muestre ESE contenido

    # ❌ No hay más contenidos en este módulo -> volvemos a lecciones sin content_id
    #    El usuario verá el listado de módulos completados
    return redirect('student:course_lessons', slug=content.module.course.slug)


# ═══════════════════════════════════════════════
# ✅ FUNCIÓN AYUDANTE: ¿El usuario está inscrito?
# ═══════════════════════════════════════════════
def user_is_enrolled(user, course: Course) -> bool:
    # Buscamos si existe un Enrollment con este usuario y curso
    is_enrolled = Enrollment.objects.filter(user=user, course=course).exists()
    # 💡 También permitimos si es staff (admin) aunque no esté inscrito formalmente
    return is_enrolled or user.is_staff


# ═══════════════════════════════════════════════
# ⭐ CREAR O EDITAR UNA RESEÑA
# ═══════════════════════════════════════════════
def review_course(request, slug):
    # ── Buscamos el curso ──
    course = get_object_or_404(Course, slug=slug)

    # ── Verificamos que el usuario esté inscrito (sino, no puede reseñar) ⛔ ──
    if not user_is_enrolled(request.user, course):
        messages.error(request, "No estas inscrito en este curso.")
        # Redirigimos al detalle del curso
        return redirect('student:course_detail', slug=course.slug)

    # ── ¿El usuario ya había reseñado este curso antes? ──
    try:
        # Intentamos obtener la reseña existente
        instance = Review.objects.get(user=request.user, course=course)
        is_update = True   # ✅ Ya existe -> estamos EDITANDO
    except Review.DoesNotExist:
        instance = None    # ❌ No existe -> estamos CREANDO una nueva
        is_update = False

    # ── Evaluamos si la petición es POST (envío del formulario) ──
    if request.method == 'POST':
        # Creamos el formulario con los datos enviados y la instancia (si existe)
        form = ReviewForm(request.POST, instance=instance)

        # ── Evaluamos si el formulario es válido ──
        if form.is_valid():
            # ✅ Válido -> guardamos la reseña (sin commit para asignar user y course)
            review = form.save(commit=False)
            review.user = request.user   # 👤 El autor es el usuario actual
            review.course = course       # 📚 El curso reseñado
            review.save()                # 💾 Guardamos en DB

            # ── Recalculamos el promedio de estrellas del curso ⭐ ──
            reviews_qs = Review.objects.filter(course=course)
            stats = reviews_qs.aggregate(
                average_rating=Avg('rating'),
                total_count=Count('id')
            )
            # Actualizamos el campo 'rating' del curso con el nuevo promedio
            course.rating = stats['average_rating']
            course.save()  # 💾 Guardamos el curso con su nuevo rating

            # ── Mostramos mensaje de éxito (según si fue creación o edición) ──
            if is_update:
                message = 'Reseña actualizada'
            else:
                message = 'Tu reseña ha sido guardada.'
            messages.success(request, message)

            # Redirigimos al detalle del curso (donde se ven las reseñas)
            return redirect('student:course_detail', slug=course.slug)

    else:
        # ❌ No es POST -> es GET, mostramos el formulario vacío o relleno
        form = ReviewForm(instance=instance)

    # ── Renderizamos el formulario de reseña ──
    return render(request, 'courses/review_course.html', {
        'is_update': is_update,  # True si es edición, False si es nueva
        'form': form,            # 📝 El formulario (con o sin datos)
        'course': course         # 📚 El curso que se está reseñando
    })