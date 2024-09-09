from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account, Product, Category, SubCategory
from django.contrib.auth.models import User
from django.core.paginator import Paginator

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
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        user_account.name = request.POST.get('name')
        user_account.surname = request.POST.get('surname')
        user_account.phone = request.POST.get('phone')
        user_account.save()

        return redirect('webshop:profile')

    return render(request, 'webshop/profile.html', {'user_account': user_account}) 

def personal_data_view(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        user_account.name = request.POST.get('name')
        user_account.surname = request.POST.get('surname')
        user_account.phone = request.POST.get('phone')
        user_account.email = request.POST.get('email')
        user_account.home_address = request.POST.get('home_address')
        iban = request.POST.get('iban')
        bank = request.POST.get('bank')
        
        if iban:  
            user_account.iban = iban
        if bank: 
            user_account.bank = bank

        user_account.save()
        return redirect('webshop:personal_data')
    
    return render(request, 'webshop/personal_data.html', {'user_account': user_account})

def orders_view(request):
    return render(request, 'webshop/orders.html')    

def returns_view(request):
    return render(request, 'webshop/returns.html')    

def payment_view(request):
    return render(request, 'webshop/payment.html') 

def delivery_view(request):
    return render(request, 'webshop/delivery.html') 

def articles_display_view(request, category_name, subcategory_name):
    category = get_object_or_404(Category, slug=category_name)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_name, category=category)
    
    products = Product.objects.filter(subcategory=subcategory)

    context = {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'products': products
    }
    
    return render(request, 'webshop/articles_display.html', context)

def sort_articles(request):
    sort_option = request.GET.get('sort', 'price_asc')
    
    if sort_option == 'newest':
        products = Product.objects.all().order_by('-created_at')
    elif sort_option == 'oldest':
        products = Product.objects.all().order_by('created_at')
    elif sort_option == 'price_asc':
        products = Product.objects.all().order_by('price')
    elif sort_option == 'price_desc':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all() 
    
    return render(request, 'webshop/articles_display.html', {'products': products})

def articles_details_view(request, product_slug):
   
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'webshop/articles_details.html', {'product': product})