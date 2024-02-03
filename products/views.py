from django.shortcuts import render, get_object_or_404

from .models import Product

# Create your views here.
def product_list(request):
    products_with_price = Product.objects.all().prefetch_related('price')
    
    context = {
        'products_with_price': products_with_price,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
