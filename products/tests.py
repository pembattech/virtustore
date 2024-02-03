from django.test import TestCase

# Create your tests here.
# products/views.py

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_POST
@csrf_exempt
def create_stripe_checkout_session(request, pk):
    """
    Create a checkout session and return the session ID
    """
    price = Price.objects.get(id=pk)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price.price) * 100,
                    "product_data": {
                        "name": price.product.name,
                        "description": price.product.desc,
                        "images": [
                            f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                        ],
                    },
                },
                "quantity": price.product.quantity,
            }
        ],
        metadata={"product_id": price.product.id},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )

    return JsonResponse({"sessionId": checkout_session.id})
