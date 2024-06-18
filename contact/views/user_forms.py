from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from contact.forms import ContactForm, RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('contact:login')
        
        if form.errors:
            messages.error(request, 'Erro ao cadastrar usuário!')
    

    return render(
        request, 
        'contact/register.html',
        {
            'form': form,
        }
    )

def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Usuário logado com sucesso!')
            return redirect('contact:index')
        

    return render(
        request, 
        'contact/login.html',
        {
            'form': form,
        }
    )

def logout_view(request):
    auth.logout(request)
    messages.info(request, 'Desconectado.')
    return redirect('contact:login')

def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request, 
            'contact/user_update.html',
            {
                'form': form,
            }
        )
    
    form = RegisterUpdateForm(instance=request.user, data=request.POST)

    if not form.is_valid():
        return render(
            request, 
            'contact/user_update.html',
            {
                'form': form,
            }
        )
    
    form.save()
    messages.success(request, 'Cadastro atualizado com sucesso!')
    return redirect('contact:user_update')
    