from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False,
        )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome',
            }
        ),
        label='First name',
        help_text='Informe o primeiro nome',
    )


    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
        )

        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Sobrenome'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Telefone'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': ''
                }
            ),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        primeiro_nome = cleaned_data.get('first_name')
        ultimo_nome = cleaned_data.get('last_name')

        if primeiro_nome == ultimo_nome:
            msg = ValidationError(
                    'O primeiro nome não pode ser igual ao último nome',
                    code='invalid'
                )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)
        

        return super().clean()
    
    def clean_first_name(self):
        cleaned_data = self.cleaned_data.get('first_name')
        if cleaned_data == 'ABC':
            self.add_error(
            'first_name',
            ValidationError(
                'Add error',
                code='invalid'
            )
        )
    
        return cleaned_data

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2
    )
    last_name = forms.CharField(
        required=True,
        min_length=2
    )

    email = forms.EmailField(
        required=True
    )


    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'email',
            'username',
            'password1',
            'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email já cadastrado.')

        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        help_text='Informe o primeiro nome',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Mínimo de 2 caracteres',
            'max_length': 'Máximo de 50 caracteres',
        }
    )

    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        help_text='Informe o último nome',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Mínimo de 2 caracteres',
            'max_length': 'Máximo de 50 caracteres',
        }
    )

    password1 = forms.CharField(
        label="Nova Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirmação de Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'email',
            'username',
        )
    
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não conferem.')
                )

        return super().clean()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError('Email já cadastrado.')

        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as e:
                self.add_error(
                    'password1',
                    ValidationError(e) 
                    )
        
        return password1
