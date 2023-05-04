from django.contrib import admin

from .models import Item, OrderItem, Order, BillingAddress, Account

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']
    list_filter = ['ordered']

    
class ItemAdmin(admin.ModelAdmin):
    list_filter = ['category']
    
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Account)