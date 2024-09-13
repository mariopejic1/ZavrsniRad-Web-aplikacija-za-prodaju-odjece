from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account, Product, Category, SubCategory, ProductVariation, Comment, Cart, CartItem, Order, Size, ProductVariationSize, Color, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.db.models import Sum

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
        city = request.POST.get('city')
        postal_number = request.POST.get('postal_number')
        street = request.POST.get('street')
        house_number = request.POST.get('house_number')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Račun s ovim emailom već postoji!')
            return render(request, 'webshop/register.html', {
                'name': name,
                'surname': surname,
                'email': email,
                'city': city,
                'postal_number': postal_number,
                'street': street,
                'house_number': house_number,
                'phone': phone,
            })

        if len(password) < 8:
            messages.error(request, 'Lozinka mora sadržavati najmanje 8 znakova!')
            return render(request, 'webshop/register.html', {
                'name': name,
                'surname': surname,
                'email': email,
                'city': city,
                'postal_number': postal_number,
                'street': street,
                'house_number': house_number,
                'phone': phone,
            })

        if password != confirm_password:
            messages.error(request, 'Lozinke se ne podudaraju!')
            return render(request, 'webshop/register.html', {
                'name': name,
                'surname': surname,
                'email': email,
                'city': city,
                'postal_number': postal_number,
                'street': street,
                'house_number': house_number,
                'phone': phone,
            })

        user = User.objects.create_user(username=email, email=email, password=password)
        Account.objects.create(
            user=user,
            name=name,
            surname=surname,
            email=email,
            phone=phone,
            city=city,
            postal_number=postal_number,
            street=street,
            house_number=house_number
        )
        messages.success(request, 'Registracija je uspješna! Sada se možete prijaviti.')
        return redirect('webshop:login')

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

def returns_view(request):
    return render(request, 'webshop/returns.html')    

def payment_view(request):
    return render(request, 'webshop/payment.html') 

def delivery_view(request):
    return render(request, 'webshop/delivery.html') 

def articles_display_view(request, category_name, subcategory_name):
    sort = request.GET.get('sort', 'price_asc')
    selected_colors = [color for color in request.GET.getlist('color') if color.isdigit()]
    selected_sizes = [size for size in request.GET.getlist('size') if size.isdigit()]

    category = get_object_or_404(Category, slug=category_name)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_name, category=category)

    products = Product.objects.filter(subcategory=subcategory)
    product_variations = ProductVariation.objects.filter(product__in=products)

    if selected_colors:
        product_variations = product_variations.filter(color__id__in=selected_colors)

    if selected_sizes:
        product_variation_sizes = ProductVariationSize.objects.filter(
            size__id__in=selected_sizes,
            is_available=True
        ).values_list('product_variation_id', flat=True)
        product_variations = product_variations.filter(id__in=product_variation_sizes)

    if sort == 'newest':
        product_variations = product_variations.order_by('-product__created_at')
    elif sort == 'oldest':
        product_variations = product_variations.order_by('product__created_at')
    elif sort == 'price_asc':
        product_variations = product_variations.order_by('product__price')
    elif sort == 'price_desc':
        product_variations = product_variations.order_by('-product__price')

    filtered_products = Product.objects.filter(variations__in=product_variations).distinct()

    context = {
        'category_name': category_name,
        'subcategory_name': subcategory_name,
        'products': filtered_products,
        'filtered_product_variations': product_variations.distinct(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'sort': sort,
    }

    return render(request, 'webshop/articles_display.html', context)

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
    
def search_view(request):
    query = request.GET.get('query', '')
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')
    selected_category = request.GET.get('category', '')
    selected_subcategory = request.GET.get('subcategory', '')
    sort = request.GET.get('sort', '')

    colors = Color.objects.all()
    sizes = Size.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    product_variations = ProductVariation.objects.all()

    if query:
        keywords = query.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects &= (
                Q(product__name__icontains=keyword) |
                Q(product__category__name__icontains=keyword) |
                Q(product__subcategory__name__icontains=keyword) |
                Q(color__name__icontains=keyword)
            )
        product_variations = product_variations.filter(q_objects).distinct()


    if selected_sizes and all(size.isdigit() for size in selected_sizes):
        product_variations = product_variations.filter(variation_sizes__size__id__in=selected_sizes, variation_sizes__is_available=True).distinct()

    if sort == 'newest':
        product_variations = product_variations.order_by('-product__created_at')
    elif sort == 'oldest':
        product_variations = product_variations.order_by('product__created_at')
    elif sort == 'price_asc':
        product_variations = product_variations.order_by('product__price')
    elif sort == 'price_desc':
        product_variations = product_variations.order_by('-product__price')

    context = {
        'filtered_product_variations': product_variations,
        'colors': colors,
        'sizes': sizes,
        'categories': categories,
        'subcategories': subcategories,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
        'query': query,
        'sort': sort,
    }

    return render(request, 'webshop/search.html', context)

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user.account)
    cart_items = cart.items_in_cart.all()

    subtotal = 0
    for item in cart_items:
        product_price = item.product.product.price  
        item_total = item.quantity * product_price  
        subtotal += item_total  

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
    return redirect('webshop:cart')  

def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user.account)

    if request.method == 'POST':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('webshop:cart')


def add_to_cart(request, category_name, subcategory_name, product_slug, color=None):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product_variation_id = request.POST.get('product_variation_id')
        size_id = request.POST.get('size')  
        
        product_variation = get_object_or_404(ProductVariation, id=product_variation_id)
        
        size = get_object_or_404(ProductVariationSize, id=size_id) if size_id else None
        
        cart, created = Cart.objects.get_or_create(user=request.user.account)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_variation,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('webshop:articles_details', category_name=category_name, subcategory_name=subcategory_name, product_slug=product_slug, color=color)
    
def create_order_view(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user.account)
        cart_items = cart.items_in_cart.all()

        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, 'Molimo vas da odaberete način plaćanja.')
            return redirect('webshop:cart')

        order = Order.objects.create(
            account=request.user.account,
            status='IP',
            payment_method=payment_method
        )

        for cart_item in cart_items:
            size_name = cart_item.size.size.name if cart_item.size else ''
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                size=size_name,
                quantity=cart_item.quantity
            )
        cart.items_in_cart.all().delete()
        
        return redirect('webshop:order_details', order_id=order.id)

    return redirect('webshop:cart')


def order_details_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items_in_order.all() 

    total_price = sum(item.total_price() for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'webshop/order_details.html', context)

def orders_history_view(request):
    orders = Order.objects.filter(account=request.user.account).order_by('-date_ordered')
    
    for order in orders:
        order.total_price = sum(item.total_price() for item in order.items_in_order.all())
    
    context = {
        'orders': orders
    }
    
    return render(request, 'webshop/orders_history.html', context)











