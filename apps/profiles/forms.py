from django import forms
from .models import Profile

TIMEZONE_CHOICES = [
    ('UTC', 'UTC'),
    ('EST', 'EST'),
    ('CST', 'CST'),
    ('MST', 'MST'),
    ('PST', 'PST'),
]

class ProfileForm(forms.ModelForm):
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