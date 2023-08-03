from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Class based views
class Home(View):

    def get(self, request):
        records = Record.objects.all()
        return render(request, 'website/home.html', {'records': records})

class RecordDetail(DetailView):
    pass

# Function based views

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

