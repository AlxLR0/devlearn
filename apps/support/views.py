from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SupportForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
class SupportView(LoginRequiredMixin, FormView):
    template_name = 'support/support.html'
    form_class = SupportForm
    success_url = reverse_lazy('support')
    
    def form_valid(self, form):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        phone = getattr(profile, 'phone', None)
        company = getattr(profile, 'company', '')
        profession = getattr(profile, 'profession', '')


        info = {
            'subject': form.cleaned_data['subject'],
            'message': form.cleaned_data['message'],
            'user_full_name': user.get_full_name() or user.username,
            'user_email': user.email,
            'phone': phone,
            'company': company,
            'profession': profession, 

        }


        body = render_to_string('support/emails/support_email.txt', info)
        to_email = getattr(settings, 'SUPPORT_INBOX', None)

        if not to_email:
            messages.error(self.request, 'Lo siento, no pudimos enviar tu mensaje en este momento. Intenta más tarde.')
            return self.form_invalid(form)

        try:

            email = EmailMessage(
                subject=f"[Soporte] {info['subject']}",
                body=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                to=[to_email],
                reply_to=[user.email] if user.email else None,
            )
            email.send(fail_silently = False)
        except Exception as e:
            messages.error(self.request, f'Error al enviar el correo: {type(e).__name__}: {e}')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Tu mensaje se ha enviado correctamente.')
        return super().form_valid(form)
    
