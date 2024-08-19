from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    home_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    GENDER_CHOICES = (
        ('M', 'Muški'),
        ('F', 'Ženski'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"User {self.id} - {self.name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    composition = models.TextField()
    origin = models.CharField(max_length=255)
    care_instructions = models.TextField()
    sizes = models.ManyToManyField('Size', through='ProductSize') 

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50) 
    is_available = models.BooleanField(default=True) 

    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock_status = models.CharField(max_length=20, choices=(
        ('IN_STOCK', 'Na zalihama'),
        ('OUT_OF_STOCK', 'Nema na zalihama'),
    ), default='IN_STOCK')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes')  
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('IP', 'U pripremi'),
        ('SP', 'Poslano'),
        ('DL', 'Dostavljeno'),
        ('RE', 'Odbijeno'),
    )
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='IP')

    def __str__(self):
        return f"Order {self.id} for {self.account.name} - Status: {self.get_status_display()}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart of {self.cart.user.username}"
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_posted')    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.user} on {self.product.name}"