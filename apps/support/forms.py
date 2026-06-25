from django import forms

# Formulario de contacto para soporte técnico 📧
class SupportForm(forms.Form):
    subject = forms.CharField(
        label='Asunto',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Asunto'})  # Placeholder: texto de ayuda dentro del campo ✍️
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Escribe tu mensaje'})  # Área de texto grande 📝
    )