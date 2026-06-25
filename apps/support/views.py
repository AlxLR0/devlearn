# ─────────────────────────────────────────────
# 📧 SOPORTE: formulario de contacto que envía un correo electrónico
# ─────────────────────────────────────────────
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin  # 🔒 Obliga a estar logueado
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SupportForm  # 📝 Formulario de soporte (vive en forms.py)
from django.template.loader import render_to_string  # 🖨️ Convierte template .txt a string
from django.core.mail import EmailMessage  # 📤 Clase para construir y enviar correos
from django.conf import settings  # ⚙️ settings.py (para leer SUPPORT_INBOX, etc.)


class SupportView(LoginRequiredMixin, FormView):
    template_name = 'support/support.html'
    form_class = SupportForm
    success_url = reverse_lazy('support')  # Al enviar, recarga la misma página

    # ── form_valid: se ejecuta cuando el formulario es VÁLIDO ──
    def form_valid(self, form):
        # ── Obtenemos datos del usuario ──
        user = self.request.user
        # Intentamos obtener el perfil (puede no existir si algo salió mal)
        profile = getattr(user, 'profile', None)
        phone = getattr(profile, 'phone', None)  # 📱 Puede ser None si no hay campo phone
        company = getattr(profile, 'company', '')
        profession = getattr(profile, 'profession', '')

        # ── Armamos un dict con toda la info para el correo ──
        info = {
            'subject': form.cleaned_data['subject'],                   # Asunto del mensaje
            'message': form.cleaned_data['message'],                   # Cuerpo del mensaje
            'user_full_name': user.get_full_name() or user.username,   # Nombre del usuario
            'user_email': user.email,                                   # Email del usuario
            'phone': phone,          # 📱 Teléfono (si tiene)
            'company': company,      # 🏢 Empresa (si tiene)
            'profession': profession, # 💼 Profesión (si tiene)
        }

        # ── Renderizamos la plantilla de correo ( .txt ) con los datos ──
        body = render_to_string('support/emails/support_email.txt', info)

        # ── ¿A dónde se envía el correo? ──
        # Se configura en settings.py > SUPPORT_INBOX o en el .env
        to_email = getattr(settings, 'SUPPORT_INBOX', None)

        # ── Evaluamos si hay una bandeja de soporte configurada ──
        if not to_email:
            # ❌ No hay destinatario -> mostramos error
            messages.error(self.request,
                           'Lo siento, no pudimos enviar tu mensaje en este momento. Intenta más tarde.')
            return self.form_invalid(form)  # Devuelve el formulario con error

        # ── Intentamos enviar el correo ──
        try:
            # Construimos el EmailMessage de Django 📤
            email = EmailMessage(
                subject=f"[Soporte] {info['subject']}",              # Asunto: "[Soporte] ..."
                body=body,                                             # Cuerpo del correo
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),  # Quién envía
                to=[to_email],                                         # Para quién
                reply_to=[user.email] if user.email else None,         # 📬 Responder al usuario
            )
            # Enviamos: fail_silently=False -> si falla, lanza excepción
            email.send(fail_silently=False)

        except Exception as e:
            # ❌ Error al enviar -> mostramos el error al usuario
            messages.error(self.request,
                           f'Error al enviar el correo: {type(e).__name__}: {e}')
            return self.form_invalid(form)

        # ✅ Todo salió bien -> mensaje de éxito
        messages.success(self.request, 'Tu mensaje se ha enviado correctamente.')
        # Llamamos al padre para que haga el redirect a success_url
        return super().form_valid(form)
    
