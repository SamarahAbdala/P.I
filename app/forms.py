# Django Imports
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Local Imports
from .models import Duvida, Comentario, Usuario

# Custom Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', max_length=150) 
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    class Meta:
        fields = ['username', 'password']

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    cpf = forms.CharField(max_length=11, required=True)  
    datanasc = forms.DateField(required=True)  

    class Meta:
        model = User
        fields = ("nome", "email", "cpf", "datanasc", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        usuario = Usuario(
            user=user,
            nome=self.cleaned_data['nome'],
            datanasc=self.cleaned_data['datanasc'],
            cpf=self.cleaned_data['cpf']
        )
        if commit:
            usuario.save()
        return user

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'datanasc', 'cpf']

# Usuario Form
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'datanasc', 'cpf'] 

# Duvida Form
class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ['titulo', 'duvida']
        labels = {
            'titulo': 'Produto',
            'duvida': 'Experiência',
        }


# Comentario Form
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
