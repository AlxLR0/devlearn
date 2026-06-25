from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm  # Formulario base de registro de Django 🔑
from .models import User  # Nuestro User personalizado (viene de models/user.py) 👤

# Opciones de zona horaria para el selector ⏰
TIMEZONE_CHOICES = [
    ('UTC', 'UTC'),
    ('EST', 'EST'),
    ('CST', 'CST'),
    ('MST', 'MST'),
    ('PST', 'PST'),
]

# Formulario para editar el perfil (usado en ProfileUpdateView) ✏️
class ProfileForm(forms.ModelForm):
    # Campos extra del User que editamos desde el perfil (no están en Profile directamente)
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = Profile
        fields = ['company', 'profession', 'timezone', 'photo']  # Campos propios de Profile
        widgets = {
            'timezone': forms.Select(choices=TIMEZONE_CHOICES),  # Select en vez de input texto
        }

    def __init__(self, *args, **kwargs):
        # ── Sacamos el 'user' de los kwargs (lo manda ProfileUpdateView.get_form_kwargs) ──
        user = kwargs.pop('user', None)  # Si no viene user, queda como None
        super(ProfileForm, self).__init__(*args, **kwargs)

        # ── Si nos pasaron un usuario, precargamos sus datos en los campos ──
        if user:
            # 💡 Esto hace que cuando se renderiza el formulario, los campos
            #    de email, nombre y apellido ya aparezcan llenos con los datos actuales
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        # Si no hay user, los campos quedan vacíos (no debería pasar)

    def save(self, commit=True):
        # ── Guardamos el Profile primero (sin commit para manipular antes) ──
        profile = super().save(commit=False)
        # Obtenemos el User asociado a este perfil
        user = self.instance.user

        # ── Sincronizamos los campos extra del formulario con el User ──
        # ⚠️ El formulario tiene campos 'email', 'first_name', 'last_name'
        #    que NO son del modelo Profile, sino del modelo User
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        # ── Evaluamos si hacemos commit (guardar en DB) o no ──
        if commit:
            # ✅ commit=True -> guardamos AMBOS: el User y el Profile
            user.save()     # Guarda los cambios en la tabla User
            profile.save()  # Guarda los cambios en la tabla Profile
        # ❌ commit=False -> no se guarda nada (el llamador decidirá después)

        # Devolvemos el perfil actualizado (ya con los cambios del User aplicados)
        return profile

# Formulario de registro personalizado (extiende el UserCreationForm de Django) ✍️
class CustomRegisterForm(UserCreationForm):
    # Agregamos campos obligatorios que Django no pide por defecto
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User  # Usamos nuestro modelo User personalizado 🎯
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        # ── Validación personalizada: correo único ──
        # Django ejecuta clean_email() automáticamente cuando se envía el formulario
        email = self.cleaned_data.get('email')  # Obtenemos el email del formulario

        # ── Buscamos en la DB si ya existe un usuario con ese email ──
        if User.objects.filter(email=email).exists():
            # ⛔ Ya existe -> lanzamos un error que Django mostrará en el formulario
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        # ✅ No existe -> devolvemos el email limpio y validado
        return email
