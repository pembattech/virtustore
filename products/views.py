from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse
import stripe

from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def product_list(request):
    products_with_price = Product.objects.all().prefetch_related("price")

    context = {
        "products_with_price": products_with_price,
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {"product": product}

    return render(request, "products/product_detail.html", context)


def create_stripe_checkout_session(request, slug):
    """
    Create a checkout session and return the session ID
    """
    

    product = get_object_or_404(Product, slug=slug)

    print(f"{settings.BACKEND_DOMAIN}{product.thumbnail.url}")

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(product.price.price) * 100,
                    "product_data": {
                        "name": product.name,
                        "description": product.desc,
                    },
                },
                "quantity": product.quantity,
            }
        ],
        metadata={"product_slug": product.slug},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )


    return redirect(checkout_session.url)

def payment_success(request):
    return render(request, 'products/payment_success.html')

def payment_cancel(request):
    return render(request, 'products/payment_cancel.html')