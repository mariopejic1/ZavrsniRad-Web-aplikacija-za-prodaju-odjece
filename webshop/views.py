from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account
from django.contrib.auth.models import User

def home_view(request):
    return render(request, 'webshop/home.html')    

def base_view(request):
    context = {}
    return render(request, 'webshop/base.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('webshop:profile')  
        else:
            messages.error(request, 'Pogrešan email ili lozinka.')
    return render(request, 'webshop/login.html')

def logout_view(request):
    logout(request)
    return redirect('webshop:login')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        home_address = request.POST.get('home_address')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Već postoji račun s ovim emailom!')
        
        elif len(password) < 8:
            messages.error(request, 'Lozinka mora biti barem 8 znakova duga!')
        
        elif password != confirm_password:
            messages.error(request, 'Lozinke se ne podudaraju!')
        
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            Account.objects.create(
                user=user,
                name=name,
                surname=surname,
                email=email,
                home_address=home_address,
                phone=phone
            )
            messages.success(request, 'Registracija uspješna! Možete se prijaviti.')
            return redirect('webshop:login')

        return render(request, 'webshop/register.html', {
            'name': name,
            'surname': surname,
            'email': email,
            'home_address': home_address,
            'phone': phone
        })

    return render(request, 'webshop/register.html')

def profile_view(request):
    return render(request, 'webshop/profile.html')    