
from .module import Module  # FK al módulo al que pertenece el contenido 📦
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey  # Relación genérica 🎭
from django.contrib.contenttypes.models import ContentType  # Catálogo de modelos de Django
from django.conf import settings
from ..fields import OrderField  # Campo personalizado para orden automático 🔢

# ─────────────────────────────────────────────
# 📦 Modelo BASE abstracto para los 4 tipos de contenido
# ─────────────────────────────────────────────
# "Abstracto" (abstract = True) significa que NO crea una tabla en la base de datos
# Solo sirve como PLANTILLA para que Text, File, Image y Video hereden sus campos
class ItemBase(models.Model):
    # %(class)s se reemplaza automáticamente: para Text será 'text_related',
    # para Video será 'video_related', etc. Así los related_name no chocan
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)                # Título del contenido 📛
    created_at = models.DateTimeField(auto_now_add=True)   # Fecha de creación (solo al insertar) 📅
    updated_at = models.DateTimeField(auto_now=True)       # Fecha de modificación (cada vez que se guarda) 🔄

    class Meta:
        abstract = True  # 🚫 No crea tabla en DB

    def __str__(self):
        return self.title

# --- Los 4 tipos concretos de contenido 📄 ---
# Cada uno hereda de ItemBase (tiene owner, title, created_at, updated_at)
# y agrega su campo específico

class Text(ItemBase):
    content = models.TextField()  # 📝 Texto enriquecido (HTML permitido)

class File(ItemBase):
    file = models.FileField(upload_to='files')  # 📎 Archivo descargable (PDF, ZIP, etc.)

class Image(ItemBase):
    file = models.FileField(upload_to='images')  # 🖼️ Imagen (JPG, PNG, etc.)

class Video(ItemBase):
    url = models.URLField()  # 🎥 URL de video (YouTube, Vimeo, etc.)

# ─────────────────────────────────────────────
# 🔗 Tabla PUENTE: conecta un Módulo con un contenido específico
# ─────────────────────────────────────────────
# Usa GenericForeignKey para apuntar a CUALQUIER tipo de contenido
# (Text, File, Image o Video) sin tener 4 campos de FK separados
class Content(models.Model):
    # ── FK al módulo al que pertenece este contenido ──
    # related_name='contents' permite hacer: modulo.contents.all()
    module = models.ForeignKey(
        Module, related_name='contents', on_delete=models.CASCADE)

    # ── content_type: guarda QUÉ tipo de contenido es ──
    # Ej: si apunta a un Text, aquí se guarda "Text"
    # limit_choices_to: solo permite text, video, image, file (nada más)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        'model__in': ('text', 'video', 'image', 'file')
    })

    # ── object_id: guarda el ID del contenido específico ──
    # Ej: si es un Text con ID 5, aquí se guarda 5
    object_id = models.PositiveIntegerField()

    # ── item: el OBJETO REAL (Text, Video, etc.) ⚡ ──
    # GenericForeignKey usa content_type + object_id para resolver el objeto
    # 📌 Así puedes hacer: content.item y obtener el Text/Video/File/Image real
    item = GenericForeignKey('content_type', 'object_id')

    # ── Orden dentro del módulo (auto-asignado, agrupado por módulo) ──
    order = OrderField(blank=True, for_fields=['module'])