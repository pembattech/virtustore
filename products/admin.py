from django.contrib import admin

from .models import Price, Product, ProductTag

class PriceAdmin(admin.StackedInline):
    model = Price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PriceAdmin,)
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Product

admin.site.register(ProductTag)
admin.site.register(Price)