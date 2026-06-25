# ─────────────────────────────────────────────
# 🏠 DASHBOARD: vista principal después de iniciar sesión
# ─────────────────────────────────────────────
from django.shortcuts import render, redirect
from apps.courses.models import Course   # Modelo Course (apps/courses/models/course.py) 📚
from apps.profiles.models import Profile # Modelo Profile (apps/profiles/models/profile.py) 👤


def index(request):
    # ── Cursos inscritos: agarramos 3 ALEATORIOS (order_by('?')) ──
    # Filtramos: solo cursos donde el usuario tiene un Enrollment
    # order_by('?') ordena aleatoriamente (lento si hay muchos registros)
    # [:3] solo los primeros 3 resultados
    courses = Course.objects.filter(
        enrollment__user=request.user
    ).order_by('?')[:3]

    # ── Perfil del usuario ──
    # 💡 Si el usuario no tiene profile, esto lanza error (pero siempre se crea al registrarse)
    profile = Profile.objects.get(user=request.user)

    # ── Último curso visitado (datos guardados en sesión desde student.py) 🔄 ──
    # course_lessons() en student.py guarda last_course_slug, last_course_title, last_course_image
    # Si el usuario nunca ha visto un curso, estos valores serán None
    last_course = {
        "slug": request.session.get('last_course_slug'),     # 🔗 Slug del último curso
        "title": request.session.get('last_course_title'),   # 📛 Título
        "image": request.session.get('last_course_image')    # 🖼️ Imagen de portada
    }

    # ── Renderizamos el dashboard con todos los datos ──
    return render(request, "dashboard/index.html", {
        'courses': courses,      # 📚 Cursos aleatorios (máx 3)
        'profile': profile,      # 👤 Perfil del usuario
        'last_course': last_course  # 🔄 Botón "seguir estudiando"
    })


def redirect_home(request):
    # ── Redirige según el ROL del usuario ──
    user = request.user

    # ── Evaluamos si el usuario es instructor ──
    # getattr con default=False: si user no tiene atributo is_instructor, asume False
    if getattr(user, 'is_instructor', False):
        # ✅ Es instructor -> va al panel de instructor
        return redirect('instructor:course_list')  # (apps/courses/urls/instructor.py)
    else:
        # ❌ Es estudiante (o no tiene rol) -> va al listado de cursos
        return redirect('student:course_list')     # (apps/courses/urls/student.py)