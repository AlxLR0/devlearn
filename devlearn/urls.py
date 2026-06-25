"""
URL configuration for devlearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
# RegisterView viene de apps/profiles/views.py, CustomPasswordChangeView también 👤
from apps.profiles.views import RegisterView, CustomPasswordChangeView

# Mapa maestro de URLs del proyecto 🗺️
urlpatterns = [
    path('admin/', admin.site.urls),                                             # Panel de administración de Django 🔧
    path('instructor/', include(("apps.courses.urls.instructor", "instructor"), namespace="instructor")),  # Zona de instructores 👨‍🏫
    path('student/', include(("apps.courses.urls.student", "student"), namespace="student")),              # Zona de estudiantes 🧑‍🎓
    path('dashboard/', include("apps.dashboard.urls")),                         # Dashboard personal 🏠
    path('profile/', include("apps.profiles.urls")),                            # Perfil de usuario 👤
    path('login/', LoginView.as_view(), name='login'),                          # Inicio de sesión 🔑
    path('logout/', LogoutView.as_view(), name='logout'),                       # Cerrar sesión 🚪
    path('register/', RegisterView.as_view(), name='register'),                 # Registro de nuevo usuario ✍️
    path('settings/password/', CustomPasswordChangeView.as_view(), name='change_password'),  # Cambiar contraseña 🔐
    path('support/', include("apps.support.urls")),                             # Página de soporte/contacto 📧
    
]


# ─────────────────────────────────────────────
# 💡 SOLO en modo DEBUG (desarrollo), Django sirve los archivos multimedia directamente
# ─────────────────────────────────────────────
# Si settings.DEBUG es True -> agregamos rutas para servir imágenes subidas (media/)
# Si settings.DEBUG es False (producción) -> NO se agregan, el servidor web (Nginx, etc.) las servirá
if settings.DEBUG:
    # static() genera las URLs necesarias para acceder a los archivos en MEDIA_ROOT
    # Ejemplo: si MEDIA_URL = '/media/', un archivo 'foto.jpg' se sirve en /media/foto.jpg
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
