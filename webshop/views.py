from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account, Product, Category, SubCategory, ProductVariation, Comment, Cart, CartItem, Order, Size, ProductVariationSize
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

def home_view(request):
    return render(request, 'webshop/home.html')    

def base_view(request):
    context = {}
    return render(request, 'webshop/base.html', context)

def female_homepage_view(request):
    context = {}
    return render(request, 'webshop/female_homepage.html', context)

def male_homepage_view(request):
    context = {}
    return render(request, 'webshop/male_homepage.html', context)

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
    
    products = Product.objects.filter(subcategory=subcategory).prefetch_related(
        'variations__images'  
    )

    context = {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'products': products
    }
    
    return render(request, 'webshop/articles_display.html', context)

def sort_articles(request, category_name, subcategory_name):
    sort_option = request.GET.get('sort', 'price_asc')
    
    category = get_object_or_404(Category, slug=category_name)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_name, category=category)
    
    products = Product.objects.filter(subcategory=subcategory)
    
    if sort_option == 'newest':
        products = products.order_by('-created_at')
    elif sort_option == 'oldest':
        products = products.order_by('created_at')
    elif sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    
    return render(request, 'webshop/articles_display.html', {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'products': products
    })

def articles_details_view(request, category_name, subcategory_name, product_slug, color):
    category = get_object_or_404(Category, slug=category_name)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_name, category=category)
    product = get_object_or_404(Product, slug=product_slug, subcategory=subcategory)

    if color:
        try:
            selected_variation = product.variations.get(color__name=color)
        except ProductVariation.DoesNotExist:
            selected_variation = product.variations.first()
    else:
        selected_variation = product.variations.first()

    variation_images = selected_variation.images.all()
    available_sizes = selected_variation.variation_sizes.filter(is_available=True)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            account = get_object_or_404(Account, user=request.user) 
            Comment.objects.create(
                product=selected_variation,
                poster=account,
                text=text,
                created_at=timezone.now()
            )
            return redirect('webshop:articles_details', category_name=category_name, subcategory_name=subcategory_name, product_slug=product_slug, color=selected_variation.color.name)

    context = {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'product': product,
        'selected_variation': selected_variation,
        'variation_images': variation_images, 
        'variations': product.variations.all(),
        'available_sizes': available_sizes
    }

    return render(request, 'webshop/articles_details.html', context)


def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user.account)
    cart_items = cart.items.all() 
    subtotal = sum(item.quantity * item.product.product.price for item in cart_items)
    delivery_cost = 0 if subtotal >= 50 else 5
    total_price = subtotal + delivery_cost
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_cost': delivery_cost,
        'total_price': total_price,
    }
    
    return render(request, 'webshop/cart.html', context)

def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity and int(new_quantity) > 0:
            item.quantity = int(new_quantity)
            item.save()
    return redirect('webshop/cart.html')

def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        item.delete()
    return redirect('webshop/cart.html')

def add_to_cart(request, category_name, subcategory_name, product_slug, color=None):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product_variation_id = request.POST.get('product_variation_id')

        # Get the ProductVariation instance
        product_variation = get_object_or_404(ProductVariation, id=product_variation_id)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user.account)

        # Get or create a CartItem for the given product variation
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_variation,  
            defaults={'quantity': quantity}
        )

        # If the cart item already exists, increase the quantity
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Redirect back to the product details page
        return redirect('webshop:articles_details', category_name=category_name, subcategory_name=subcategory_name, product_slug=product_slug, color=color)

