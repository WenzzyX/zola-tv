from django import forms
from users.models import CustomUser


class RegisterForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('phone', 'email', 'password')
