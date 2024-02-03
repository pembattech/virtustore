from django.urls import path

from .views import product_list, product_detail

app_name = "product"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("product/<slug>", product_detail, name = "product_detail")
]
