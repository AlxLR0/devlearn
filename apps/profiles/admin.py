from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Traemos nuestros modelos del paquete models/ (el __init__.py los exporta) 📦
from .models import User, InstructorProfile, Profile

# Personalizamos cómo se ve el User en el panel de administración 🛠️
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Agregamos el campo is_instructor a la pantalla de detalle del usuario ✏️
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol personalizado', {'fields': ('is_instructor',)}),
    )
    
    # También lo agregamos a la pantalla de crear usuario nuevo ➕
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields':('is_instructor',)}),
    )
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Columnas visibles en el listado de perfiles 📋
    list_display = ('user', 'company', 'profession', 'timezone', 'photo')


admin.site.register(InstructorProfile)  # Registro simple, sin personalización extra
