# ─────────────────────────────────────────────
# 📡 SEÑALES DE DJANGO: se ejecutan automágicamente cuando algo pasa en la DB
# ─────────────────────────────────────────────
from django.db.models.signals import post_save  # Se dispara "después de guardar" un registro
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile, Profile  # Nuestros modelos 📦
from django.contrib.auth import get_user_model

User = get_user_model()

# ─────────────────────────────────────────────
# 🎯 SEÑAL 1: Cuando se CREA un usuario nuevo
# ─────────────────────────────────────────────
# post_save significa: "ejecuta esto justo después de que se guarde un User en la DB"
# sender=User -> solo reacciona cuando el modelo User se guarda
# instance -> el usuario que se acaba de guardar
# created -> True si es un registro NUEVO, False si es una actualización
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # ── Evaluamos si es un usuario nuevo o una actualización ──
    if created:
        # ✅ Es un usuario NUEVO -> le creamos su Profile automáticamente
        # get_or_create: si ya existe (por alguna razón) no lo duplica
        Profile.objects.get_or_create(user=instance)
    # ❌ Si no es created (es una actualización), no hacemos nada
    #    El Profile ya debería existir desde el registro inicial

# ─────────────────────────────────────────────
# 🎯 SEÑAL 2: Cuando se guarda un usuario que es instructor
# ─────────────────────────────────────────────
@receiver(post_save, sender=User)
def create_or_update_instructor_profile(sender, instance, created, **kwargs):
    # ── Evaluamos si el usuario tiene marcado el check de instructor ──
    if instance.is_instructor:
        # ✅ Es instructor -> le creamos (o actualizamos) su InstructorProfile
        # get_or_create: si el perfil ya existe, lo deja como está
        InstructorProfile.objects.get_or_create(user=instance)
    # ❌ Si no es instructor, no hacemos nada
    #    El InstructorProfile no se elimina automáticamente si desmarca la casilla
