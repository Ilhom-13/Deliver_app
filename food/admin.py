from django.contrib import admin
from .models import  Item, Category, Order, Restaurant, Adress


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_price', 'item_owner', 'item_category']
    list_filter = ['category', 'owner']
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}

    @admin.display(description='price')
    def item_price(self, obj):
        return f'{obj.price} $'

    @admin.display(description='restaurant')
    def item_owner(self, obj):
        return f'{obj.owner.name} '\

    @admin.display(description='category')
    def item_category(self, obj):
        return f'{obj.category.name} '

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_items', 'total_price', 'date', 'status', 'user']
    list_filter = ['status', 'user', 'date']

    @admin.display(description='items')
    def get_items(self, obj):
        return ",  ".join([item.name for item in obj.items.all()])


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'open_at', 'close_at', 'day_off','contact', 'email', 'adress']
    search_fields = ['name']

    @admin.display
    def adress(self, obj):
        return obj.adress

@admin.register(Adress)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['city', 'district', 'place']

admin.site.register(Category)
