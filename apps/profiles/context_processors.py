# ─────────────────────────────────────────────
# 🖼️ CONTEXT PROCESSOR: inyecta la foto de perfil en TODAS las plantillas
# ─────────────────────────────────────────────
# Esto está registrado en settings.py > TEMPLATES > OPTIONS > context_processors
# Cada vez que Django renderiza CUALQUIER template, ejecuta esta función
# y el resultado (dict) se mezcla con las variables disponibles en la plantilla
def profile_picture(request):
    # ── Evaluamos: ¿el usuario está logueado y tiene un perfil? ──
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        # ✅ Sí -> agarramos el campo 'photo' del perfil
        photo = request.user.profile.photo
    else:
        # ❌ No (usuario anónimo o sin perfil) -> photo = None
        photo = None

    # ── Devolvemos un diccionario con la URL de la foto ──
    # Si photo existe y tiene URL -> la usamos
    # Si no -> mandamos un placeholder (imagen por defecto de avatar)
    # 💡 Esto significa que en TODAS las plantillas puedes usar {{ profile_picture }}
    #    para mostrar la foto de perfil del usuario actual
    return {
        'profile_picture': photo.url if photo else "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg"
    }
