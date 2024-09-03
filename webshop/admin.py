from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'email', 'phone', 'iban', 'bank')
    search_fields = ('user__username', 'name', 'surname', 'email', 'phone', 'iban')

    def delete_model(self, request, obj):
        user = obj.user
        super().delete_model(request, obj)  
        user.delete() 
        
admin.site.register(Account, AccountAdmin)