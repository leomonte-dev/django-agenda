from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from contact.forms import ContactForm


def create(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        context = {
        'form': form
        }

        if form.is_valid():
            form.save()
            return redirect('contact:index')
        
        return render(request, 'contact/create.html', context)
    
    context = {
        'form': ContactForm(),
    }

    return render(request, 'contact/create.html', context)

    

