from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# ─────────────────────────────────────────────
# 🎯 CAMPO PERSONALIZADO: Asigna número de orden automáticamente
# ─────────────────────────────────────────────
# Ejemplo: cuando creas un Módulo, este campo se llena SOLO con el siguiente número
# Si for_fields=['course'], el orden se reinicia por cada curso (no es global)
# Es un PositiveIntegerField (solo números positivos) con superpoderes 🔢
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        # for_fields: lista de campos que "agrupan" el orden
        # Ej: for_fields=['course'] -> el orden se calcula DENTRO de cada curso
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    # ── pre_save se ejecuta ANTES de guardar el modelo en la DB ──
    # model_instance: el objeto que se va a guardar (ej: un Module)
    # add: True si es nuevo, False si es actualización
    def pre_save(self, model_instance, add):
        # ── Evaluamos si el campo de orden está vacío (None) ──
        if getattr(model_instance, self.attname) is None:
            # ✅ Está vacío -> calculamos el orden automáticamente
            try:
                # 1️⃣ Obtenemos TODOS los registros de este modelo (ej: todos los Module)
                qs = self.model.objects.all()

                # 2️⃣ Si hay campos de agrupación (for_fields), filtramos
                #    Ej: for_fields=['course'] -> solo módulos del MISMO curso
                if self.for_fields:
                    # Construye un dict: {'course': <id_del_curso>}
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)  # Filtra: solo registros del mismo grupo

                # 3️⃣ Buscamos el registro con el orden MÁS ALTO del grupo 🔍
                last_item = qs.latest(self.attname)
                # 4️⃣ Le sumamos 1 al orden más alto encontrado
                value = getattr(last_item, self.attname) + 1

            except ObjectDoesNotExist:
                # ❌ No hay registros previos en este grupo -> empezamos desde 0
                value = 0

            # 5️⃣ Asignamos el valor calculado al campo del objeto
            setattr(model_instance, self.attname, value)
            # Devolvemos el valor para que Django lo guarde en la DB
            return value

        else:
            # ❌ El campo ya tiene un valor (lo puso el usuario manualmente)
            #    -> lo respetamos y dejamos que Django haga lo normal
            return super().pre_save(model_instance, add)