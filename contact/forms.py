from django import forms
from django.core.exceptions import ValidationError
from . import models

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }
        ),
        label='Primeiro Nome',
        help_text='Informe o primeiro nome',
    )


    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category'
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
    
 
