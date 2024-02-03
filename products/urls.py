from django.urls import path

from .views import product_list, product_detail, create_stripe_checkout_session

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("product/<slug>", product_detail, name = "product_detail"),
    path("create-checkout-session/<slug>/",create_stripe_checkout_session,name="create-checkout-session",),
]
