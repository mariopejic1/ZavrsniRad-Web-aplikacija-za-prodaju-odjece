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


# Registracija modela za kategorije
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Automatski generiraj slug na temelju imena

# Registracija modela za podkategorije
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

# Registracija modela za proizvode
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category', 'available_colors', 'available_sizes')
    search_fields = ('name', 'category__name')
    
# Registracija modela za slike proizvoda
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

# Registracija modela za boje
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Registracija modela za veličine
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available')

# Registracija modela za kombinacije boja i veličina proizvoda
@admin.register(ProductColorSize)
class ProductColorSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size')