# ─────────────────────────────────────────────
# 👨‍🏫 VISTAS DEL INSTRUCTOR (CRUD completo)
# ─────────────────────────────────────────────
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from ..models import Course, Module, Content, Text, Image, File, Video  # Modelos de courses/ 👈
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.forms.models import modelform_factory       # Crea formularios sobre la marcha ⚡
from django.contrib.contenttypes.models import ContentType  # Catálogo de modelos de Django 🎭
from django.http import HttpResponseForbidden, JsonResponse
import json

# ─────────────────────────────────────────────
# 🗺️ Mapa: nombre del modelo (string) -> clase del modelo
# Se usa para crear contenido dinámico según el tipo elegido
# ─────────────────────────────────────────────
CONTENT_MODELS = {
    'text': Text,
    'image': Image,
    'file': File,
    'video': Video
}

# ─────────────────────────────────────────────
# 👑 Mixin: solo usuarios autorizados (superuser o instructor)
# ─────────────────────────────────────────────
# LoginRequiredMixin -> si no está logueado, redirige al login
# UserPassesTestMixin -> ejecuta test_func(), si da False -> 403
class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # ── Evaluamos: ¿el usuario puede acceder? ──
        # ✅ True si es superadmin O tiene is_instructor = True
        # ❌ False si es un estudiante normal
        return self.request.user.is_superuser or self.request.user.is_instructor


# ═══════════════════════════════════════════════
# 📚 CRUD DE CURSOS
# ═══════════════════════════════════════════════

class CourseListView(InstructorRequiredMixin, ListView):
    # Muestra SOLO los cursos del instructor actual (no los de otros)
    model = Course
    template_name = 'instructor/course_list.html'  # Renderiza esta plantilla
    context_object_name = "courses"                # Variable en la plantilla: {{ courses }}
    paginate_by = 8                                # 8 cursos por página 📄

    def get_queryset(self):
        # ── Filtramos: solo cursos donde el owner sea el usuario actual ──
        # 💡 Así un instructor NO ve los cursos de otro instructor
        return Course.objects.filter(owner=self.request.user)


class CourseCreateView(InstructorRequiredMixin, CreateView):
    # Formulario para crear un nuevo curso
    model = Course
    fields = ['title', 'slug', 'overview', 'image', 'level', 'duration', 'categories']
    template_name = 'instructor/course_form.html'
    success_url = reverse_lazy('instructor:course_list')  # Al guardar, va al listado

    def form_valid(self, form):
        # ── Se ejecuta cuando el formulario es VÁLIDO ──
        # Antes de guardar, asignamos el dueño del curso
        form.instance.owner = self.request.user  # El instructor actual es el dueño 🎯
        # Llamamos al padre para que guarde y redirija
        return super().form_valid(form)


class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    # Editar un curso existente
    model = Course
    fields = ['title', 'slug', 'overview', 'image', 'level', 'duration', 'categories']
    template_name = 'instructor/course_form.html'
    success_url = reverse_lazy('instructor:course_list')

    def get_queryset(self):
        # ── Filtramos: solo puede editar SUS propios cursos ──
        return Course.objects.filter(owner=self.request.user)


class CourseDeleteView(InstructorRequiredMixin, DeleteView):
    # Eliminar un curso (pide confirmación)
    model = Course
    template_name = 'instructor/course_confirm_delete.html'
    success_url = reverse_lazy('instructor:course_list')

    def get_queryset(self):
        # ── Filtramos: solo puede eliminar SUS propios cursos ──
        return Course.objects.filter(owner=self.request.user)


# ═══════════════════════════════════════════════
# 🧩 CRUD DE MÓDULOS
# ═══════════════════════════════════════════════

class ModuleListView(InstructorRequiredMixin, ListView):
    # Lista los módulos de un curso específico
    model = Module
    template_name = 'instructor/module_list.html'
    context_object_name = "modules"

    def get_queryset(self):
        # ── Obtenemos el curso desde la URL (course_id) ──
        # get_object_or_404: si no existe o no es del instructor, da 404
        self.course = get_object_or_404(
            Course, id=self.kwargs['course_id'], owner=self.request.user)
        # Devolvemos solo los módulos de ESE curso, ordenados
        return self.course.modules.all().order_by('order')

    def get_context_data(self, **kwargs):
        # ── Agregamos el curso al contexto para usarlo en la plantilla ──
        context = super().get_context_data(**kwargs)
        context['course'] = self.course  # 💡 En template: {{ course.title }}
        return context


class ModuleCreateView(InstructorRequiredMixin, CreateView):
    # Crear un nuevo módulo DENTRO de un curso
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'

    def form_valid(self, form):
        # ── Antes de guardar, asignamos el curso al módulo ──
        course = get_object_or_404(
            Course, id=self.kwargs['course_id'], owner=self.request.user)
        form.instance.course = course  # El módulo pertenece a este curso
        return super().form_valid(form)

    def get_success_url(self):
        # ── Después de crear, volvemos al listado de módulos del mismo curso ──
        return reverse('instructor:module_list', args=[self.object.course.id])


class ModuleUpdateView(InstructorRequiredMixin, UpdateView):
    # Editar un módulo
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'

    def get_queryset(self):
        # ── Solo puede editar módulos de cursos que sean SUYOS ──
        return Module.objects.filter(course__owner=self.request.user)

    def get_success_url(self):
        return reverse('instructor:module_list', args=[self.object.course.id])


class ModuleDeleteView(InstructorRequiredMixin, DeleteView):
    # Eliminar un módulo
    model = Module
    template_name = 'instructor/module_confirm_delete.html'

    def get_queryset(self):
        return Module.objects.filter(course__owner=self.request.user)

    def get_success_url(self):
        return reverse('instructor:module_list', args=[self.object.course.id])


# ═══════════════════════════════════════════════
# 📦 CRUD DE CONTENIDOS (la parte más compleja)
# ═══════════════════════════════════════════════

class ContentListView(InstructorRequiredMixin, ListView):
    # Lista los contenidos de un módulo específico
    model = Content
    template_name = 'instructor/content_list.html'
    context_object_name = "contents"

    def get_queryset(self):
        # ── Obtenemos el módulo desde la URL ──
        self.module = get_object_or_404(
            Module, id=self.kwargs['module_id'], course__owner=self.request.user)
        # Devolvemos sus contenidos ordenados, con el content_type precargado (optimización)
        # select_related('content_type') evita consultas N+1 al mostrar el tipo
        return self.module.contents.all().select_related('content_type').order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module  # Pasamos el módulo al template
        return context


# ─── Vista HÍBRIDA: Crear o Actualizar contenido ───
# Soporta los 4 tipos (Text, File, Image, Video) usando GenericForeignKey
class ContentCreateUpdateView(InstructorRequiredMixin, View):
    template_name = 'instructor/content_form.html'

    def get_model(self, model_name):
        # ── Traduce: 'text' -> Text, 'video' -> Video, etc. ──
        # Si el model_name no existe en CONTENT_MODELS, devuelve None
        return CONTENT_MODELS.get(model_name, None)

    def get_form(self, model, *args, **kwargs):
        # ── Crea un formulario AUTOMÁTICO para cualquier modelo ──
        # modelform_factory genera un ModelForm con todos los campos del modelo,
        # excepto 'owner', 'created_at', 'updated_at' (se asignan solos)
        Form = modelform_factory(model, exclude=['owner', 'created_at', 'updated_at'])
        return Form(*args, **kwargs)

    # ── dispatch: se ejecuta SIEMPRE antes de get() o post() ──
    # Aquí pre-cargamos datos que ambas necesitan
    def dispatch(self, request, module_id=None, model_name=None, id=None, *args, **kwargs):
        # 1️⃣ Cargamos el módulo (y verificamos que sea del instructor)
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)

        # 2️⃣ Obtenemos la clase del modelo ('text' -> Text)
        self.model = self.get_model(model_name)

        # 3️⃣ Por defecto, no hay objeto (creación)
        self.obj = None

        # 4️⃣ Si viene un 'id' en la URL -> es una EDICIÓN 🆚
        if id:
            # ── Buscamos el contenido existente ──
            try:
                # Buscamos en la tabla Content que tenga:
                # - object_id = id
                # - content_type = el tipo correspondiente (Text, Video, etc.)
                # - module = el módulo actual
                content = Content.objects.select_related('content_type').get(
                    object_id=id,
                    content_type=ContentType.objects.get_for_model(self.model),
                    module=self.module
                )
                # Si existe, obtenemos el objeto real (Text, Video, etc.)
                self.obj = content.item  # 📌 El objeto concreto
            except Content.DoesNotExist:
                # ❌ No existe o no coincide -> denegamos el acceso
                return HttpResponseForbidden("No tienes permiso o tipo invalido")

        # 5️⃣ Continuamos con el flujo normal (get o post)
        return super().dispatch(request, module_id, model_name, id, *args, **kwargs)

    # ── GET: Mostrar formulario (vacío o relleno) ──
    def get(self, request, module_id, model_name, id=None):
        # Creamos el formulario con o sin instancia según si es creación/edición
        form = self.get_form(self.model, instance=self.obj)
        # Renderizamos el template con el formulario
        # 💡 'object': si es edición, contiene el Text/Video/etc. existente
        return render(request, self.template_name, {'form': form, 'object': self.obj})

    # ── POST: Procesar formulario enviado ──
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST, files=request.FILES)

        # ── Evaluamos si el formulario es válido ──
        if form.is_valid():
            # ✅ Válido -> guardamos
            # commit=False -> crea el objeto pero NO lo guarda en DB todavía
            obj = form.save(commit=False)
            # Asignamos el dueño (el instructor actual)
            obj.owner = request.user
            # Ahora sí, guardamos en DB 💾
            obj.save()

            # ── Si es CREACIÓN (no tiene id), creamos el Content que lo relaciona ──
            if not id:
                # Este es el paso clave: creamos el registro Content que vincula
                # el módulo con el nuevo objeto (Text, Video, etc.)
                Content.objects.create(module=self.module, item=obj)
            # Si tiene id -> es EDICIÓN, ya existe el Content, solo actualizamos el obj

            # Redirigimos al listado de contenidos del módulo
            return redirect('instructor:content_list', module_id=self.module.id)

        # ❌ Si el formulario NO es válido -> lo mostramos de nuevo con errores
        return render(request, self.template_name, {'form': form, 'object': self.obj})


class ContentDeleteView(InstructorRequiredMixin, DeleteView):
    # Eliminar un contenido
    model = Content
    template_name = 'instructor/content_confirm_delete.html'

    def get_queryset(self):
        return Content.objects.filter(module__course__owner=self.request.user)

    def get_success_url(self):
        return reverse('instructor:content_list', args=[self.object.module.id])


# ═══════════════════════════════════════════════
# 🔄 VISTAS DE REORDENAMIENTO (Drag & Drop vía AJAX)
# ═══════════════════════════════════════════════

class ModuleOrderView(InstructorRequiredMixin, View):
    # Recibe JSON con el nuevo orden de módulos (desde drag & drop en JS)
    def post(self, request, *args, **kwargs):
        # ── Intentamos procesar el orden ──
        try:
            # Parseamos el cuerpo JSON de la petición
            data = json.loads(request.body)
            order = data.get('order', [])  # Lista de IDs en el nuevo orden

            # ── Recorremos la lista: cada posición es el nuevo orden ──
            # Ej: order = [4, 2, 5, 3]
            # Módulo ID 4 -> order = 0
            # Módulo ID 2 -> order = 1
            # Módulo ID 5 -> order = 2
            # Módulo ID 3 -> order = 3
            for index, module_id in enumerate(order):
                Module.objects.filter(
                    id=module_id,
                    course__owner=request.user  # Solo módulos del instructor
                ).update(order=index)  # Actualizamos sin disparar señales

            # ✅ Éxito
            return JsonResponse({'status': 'ok'})

        except Exception as e:
            # ❌ Error (JSON inválido, módulo no encontrado, etc.)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ContentOrderView(InstructorRequiredMixin, View):
    # Recibe JSON con el nuevo orden de contenidos (desde drag & drop en JS)
    def post(self, request, *args, **kwargs):
        # ── Intentamos procesar el orden ──
        try:
            data = json.loads(request.body)
            order = data.get('order', [])  # Lista de IDs de contenidos

            for index, content_id in enumerate(order):
                # Actualizamos el campo 'order' de cada contenido
                Content.objects.filter(
                    id=content_id,
                    module__course__owner=request.user  # Solo contenidos del instructor
                ).update(order=index)

            return JsonResponse({'status': 'ok'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ContentOrderView(InstructorRequiredMixin, View):
    # Recibe un orden nuevo para los contenidos (vía AJAX) y lo guarda 📤
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order = data.get('order', [])

            for index, content_id in enumerate(order):
                Content.objects.filter(
                    id=content_id, module__course__owner=self.request.user).update(order=index)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ContentOrderView(InstructorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order = data.get('order', [])

            # {2,3,4,5} -> {0: 4,1: 2,5,3}
            for index, content_id in enumerate(order):
                Content.objects.filter(
                    id=content_id, module__course__owner=request.user).update(order=index)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
