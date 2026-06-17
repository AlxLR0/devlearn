from django import forms


class SupportForm(forms.Form):
    subject = forms.CharField(label='Asunto', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Asunto'}))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'rows':6, 'placeholder': 'Escribe tu mensaje'}))