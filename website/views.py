from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Model, Q

from .forms import SignUpForm, AddRecordForm, AddGroupForm
from .models import Record, UserGroup

# Class based views
class Home(LoginRequiredMixin, View):
    def get(self, request):
        user_groups = request.user.user_groups.all()
        user_records = Record.objects.filter(creator=request.user)
        group_records = Record.objects.filter(group_records__in=user_groups)

        records = group_records | user_records
        return render(request, 'website/home.html', {'records': records})

class RecordDetail(LoginRequiredMixin, DetailView):
    model = Record
    template_name = 'website/record_detail.html'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        pk = self.kwargs['pk']
        return Record.objects.get(pk=pk)
    
class AddRecord(LoginRequiredMixin, View):
    def get(self, request):
        form = AddRecordForm()
        return render(request, 'website/add_record.html', {'form': form})

    def post(self, request):
        form = AddRecordForm(request.POST, user=request.user)
        if form.is_valid():
            add_record = form.save()
            messages.success(request, f'Record "{add_record}" added')
            return redirect("home")

class UpdateRecord(LoginRequiredMixin, View):
    def get(self, request, pk):
        current_record = Record.objects.get(pk=pk)
        form = AddRecordForm(instance=current_record)

        return render(request, 'website/update_record.html', {'form': form, 'id': current_record.id})

    def post(self, request, pk):
        current_record = Record.objects.get(pk=pk)
        form = AddRecordForm(request.POST, instance=current_record)
        if form.is_valid():
            add_record = form.save()
            messages.success(request, f'Request "{add_record}" updated')
        return redirect('home')

class CreateUserGroup(LoginRequiredMixin, View):
    def get(self, request):
        form = AddGroupForm(user=request.user)
        return render(request, 'website/create_group.html', {"form": form})

    def post(self, request):
        form = AddGroupForm(request.POST, user=request.user)
        if form.is_valid():
            user_group = form.save()

            messages.success(request, f"Group {user_group} created")
            return redirect('home')
        else:
            messages.error(request, "There was an error creating the group")
            return redirect("create_group")
        
class UserGroupLists(ListView):
    model = UserGroup
    template_name = 'website/usergroup_list.html'
    context_object_name = 'groups'
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Any]:
        queryset = UserGroup.objects.prefetch_related('admin')
        
        # Filter by public groups or groups you're in
        user = self.request.user
        queryset = queryset.filter(Q(visibility='public') | (Q(admin=user) | Q(members=user)))

        return queryset

# Adicionar botão para acessar o grupo e editar, checar permissão de admin para poder editar
# Qualquer um pode adicionar pessoas no grupo.
class UserGroupDetail(DetailView):
    model = UserGroup
    template_name = 'website/usergroup_detail.html'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        pk = self.kwargs['pk']
        return UserGroup.objects.get(pk=pk)
    
class UpdateUserGroup(View):
    
    def get(self, request, pk):
        current_group = UserGroup.objects.get(pk=pk)
        form = AddGroupForm(instance=current_group)

        return render(request, 'website/update_usergroup.html', {'form': form, 'id': current_group.id})
    
    def post(self, request, pk):

        current_group = UserGroup.objects.get(pk=pk)
        form = AddGroupForm(request.POST, instance=current_group)

        if form.is_valid():
            add_group = form.save()
            messages.success(request, f'Group "{add_group}" updated')
        return redirect('home')

# Function based views

def delete_user_group(request, pk):
    user_group = UserGroup.objects.get(pk=pk)
    user_group.delete()
    messages.success(request, f"Group {user_group} deleted!")
    return redirect('home')

def add_user_to_group():
    pass

def remove_user_from_group():
    pass

def add_record_to_group():
    pass

def remove_record_from_group():
    pass

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

