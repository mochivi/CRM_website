from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Class based views
class Home(View):
    def get(self, request):
        return render(request, 'website/home.html', {})

# Function based views (simpler pages)

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
    


    return render(request, 'website/register.html', {})
