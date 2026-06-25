# Importamos herramientas de Django necesarias 🛠️
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin       # Obliga a estar logueado 🔒
from django.contrib.auth.views import PasswordChangeView        # Vista para cambiar contraseña 🔐
from django.contrib.messages.views import SuccessMessageMixin   # Muestra mensajes de éxito 💬
from django.views.generic.edit import UpdateView , CreateView   # Vistas genéricas para crear/editar ✍️
from .models import Profile                                     # Modelo Profile (1 por usuario) 👤
from .forms import ProfileForm, CustomRegisterForm              # Formularios personalizados 📝
from django.urls import reverse_lazy                            # Para URLs con lazy loading 🔗
from django.contrib import messages                             # Sistema de mensajes flash 📨
from django.shortcuts import redirect


def index(request):
    # Vista simple de perfil (renderiza la plantilla) 🖼️
    return render(request, 'profiles/profile.html')

# ─────────────────────────────────────────────
# ✏️ Vista para EDITAR el perfil del usuario
# ─────────────────────────────────────────────
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile.html'
    success_url = reverse_lazy('profile')  # redirige a sí misma después de guardar

    def get_object(self, queryset=None):
        # ── ¿Qué perfil vamos a editar? ──
        # En vez de usar un pk de la URL, agarramos el perfil del usuario logueado
        # 💡 Así el usuario NO puede editar el perfil de otro (seguridad)
        return self.request.user.profile
    
    def get_form_kwargs(self):
        # ── Le mandamos datos extra al formulario ──
        # Obtenemos los kwargs por defecto (form_class, instance, etc.)
        kwargs = super().get_form_kwargs()
        # Le inyectamos el usuario actual para que ProfileForm.__init__ lo reciba
        # y pueda precargar email, first_name, last_name
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # ── Agregamos variables extra al template ──
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # ── Evaluamos si el perfil tiene foto ──
        if profile.photo:
            # ✅ Tiene foto -> mandamos su URL
            context['profile_picture'] = profile.photo.url
        else:
            # ❌ No tiene foto -> mandamos un avatar por defecto
            context['profile_picture'] = "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg"
        # 💡 Esta variable se usará en el template como {{ profile_picture }}
        return context
    
    def form_valid(self, form):
        # ── ¿Qué pasa cuando el formulario se guarda correctamente? ──
        # Mostramos un mensaje flash de éxito (aparece en la siguiente página) ✅
        messages.success(self.request, 'Tu perfil se ha actualizado correctamente!')
        # Llamamos al form_valid del padre que guarda el objeto y redirige a success_url
        return super().form_valid(form)

# ─────────────────────────────────────────────
# ✍️ Vista de REGISTRO de nuevo usuario
# ─────────────────────────────────────────────
class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('student:course_list')  # después de registrarse va a cursos

    def form_valid(self, form):
        # ── El formulario es válido: creamos el usuario ──
        user = form.save()          # Guarda el nuevo User en la DB 🆕
        # ── Lo logueamos automáticamente (no tiene que hacer login después) ──
        login(self.request, user)   # Crea la sesión para este usuario 🔑
        # ── Redirigimos al listado de cursos ──
        return redirect(self.success_url)  # -> 'student:course_list'
    
# Vista para cambiar la contraseña desde el panel de ajustes 🔐
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'settings/change_password.html'
    success_message = "Tu contraseña ha sido cambiada correctamente"
    success_url = reverse_lazy('change_password')
