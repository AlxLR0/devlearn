from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import User

TIMEZONE_CHOICES = [
    ('UTC', 'UTC'),
    ('EST', 'EST'),
    ('CST', 'CST'),
    ('MST', 'MST'),
    ('PST', 'PST'),
]

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = Profile
        fields = ['company', 'profession', 'timezone', 'photo']
        widgets = {
            'timezone': forms.Select(choices=TIMEZONE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial=user.email
            self.fields['first_name'].initial=user.first_name
            self.fields['last_name'].initial=user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile.save()

        return profile

class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email