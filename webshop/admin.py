from django.contrib import admin
from .models import (
    Account, Category, SubCategory, Color, Size, Product, ProductVariationImage,
    ProductVariation, ProductVariationSize, Comment, CartItem, Order
)

class ProductVariationImageInline(admin.TabularInline):
    model = ProductVariationImage
    extra = 1

class ProductVariationSizeInline(admin.TabularInline):
    model = ProductVariationSize
    extra = 1

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'email', 'phone')
    search_fields = ('name', 'surname', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'created_at', 'reference_number')
    search_fields = ('name', 'reference_number')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'subcategory')

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'main_image')
    list_filter = ('product', 'color')
    search_fields = ('product__name', 'color__name')
    inlines = [ProductVariationImageInline, ProductVariationSizeInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('poster', 'product', 'text', 'created_at')  
    
admin.site.register(Comment, CommentAdmin)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')  
    list_filter = ('cart', 'product')  

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'account', 'date_ordered', 'status', 'payment_method')
    list_filter = ('status', 'payment_method')
    search_fields = ('order_number', 'account__name', 'account__surname')
    list_editable = ('status',)  

    def save_model(self, request, obj, form, change):
        if not obj.pk and request.user.is_superuser:
            obj.account = request.user.account
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
