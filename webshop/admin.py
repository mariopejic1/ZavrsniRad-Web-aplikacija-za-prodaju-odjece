from django.contrib import admin
from .models import Account, Category, SubCategory, Product, ProductImage, Color, Size, ProductColorSize

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'email', 'phone', 'iban', 'bank')
    search_fields = ('user__username', 'name', 'surname', 'email', 'phone', 'iban')

    def delete_model(self, request, obj):
        user = obj.user
        super().delete_model(request, obj)  
        user.delete() 
        
admin.site.register(Account, AccountAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductColorSizeInline(admin.TabularInline):
    model = ProductColorSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory')
    search_fields = ('name', 'category__name', 'subcategory__name')
    inlines = [ProductImageInline, ProductColorSizeInline]  # Spoji inline obrasce

admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)