from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Model

from .forms import SignUpForm
from .models import Record

# Class based views
class Home(View):

    def get(self, request):
        records = Record.objects.all()
        return render(request, 'website/home.html', {'records': records})

class RecordDetail(LoginRequiredMixin, DetailView):
    model = Record
    template_name = 'website/record_detail.html'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        pk = self.kwargs['pk']
        return Record.objects.get(pk=pk)

# Function based views

@login_required(redirect_field_name="login")
def delete_record(request, pk):
    delete_it = Record.objects.get(pk=pk)
    delete_it.delete()
    messages.success(request, f"Record for {delete_it} deleted succesfully")
    return redirect("home")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate user and redirect to homepage
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in, redirecting to homepage')
            return redirect('home')
        else:
            messages.success(request, """There was an error logging in, try again or register""")
    
    else:
        pass

    return render(request, 'website/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Authenticate and login
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "You have registered!")
            
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'website/register.html', {'form': form})

