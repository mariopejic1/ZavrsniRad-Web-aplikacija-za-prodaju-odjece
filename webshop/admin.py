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
    list_display = ('get_name', 'category')

    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'SubCategory Name'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductColorSizeInline(admin.TabularInline):
    model = ProductColorSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory')
    search_fields = ('name', 'category__name', 'subcategory__name')
    inlines = [ProductImageInline, ProductColorSizeInline]  

admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)

def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcategory":
            kwargs["queryset"] = SubCategory.objects.all()  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)