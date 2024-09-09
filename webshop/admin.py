from django.contrib import admin
from .models import (
    Account, Category, SubCategory, Color, Size, Product, ProductVariationImage,
    ProductVariation, ProductVariationSize
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

