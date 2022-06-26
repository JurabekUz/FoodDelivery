from django.contrib import admin

from .models import MenuItem,Category,OrderModel

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)


class PurchaseOrderAdmin(admin.ModelAdmin):
    fields = ['product', 'dollar_amount']
    list_display = ('get_products', 'vendor')

    def get_products(self, obj):
        return "\n".join([p.products for p in obj.product.all()])
