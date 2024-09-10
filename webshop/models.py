from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import uuid

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    home_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    iban = models.CharField(max_length=34, blank=True, null=True)  
    bank = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"User {self.id} - {self.name} - {self.surname}"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Color(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50) 

    def __str__(self):
        return self.name
     
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    composition = models.TextField()
    origin = models.CharField(max_length=255)
    care_instructions = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    reference_number = models.CharField(max_length=100, unique=False, default=uuid.uuid4, editable=False)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, through='ProductVariationSize')

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"
    
class ProductVariationImage(models.Model):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_variation_images/')
    
    def __str__(self):
        return f"Image for {self.product_variation.product.name} - {self.product_variation.color.name} - Image"
    
class ProductVariationSize(models.Model):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='variation_sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_variation.product.name} - {self.product_variation.color.name} - {self.size.name}"
    
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
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='comments')
    poster = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comments_posted')    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.poster.name}"