from django.db import models
from django.template.defaultfilters import slugify

from .helper import generate_slug


def get_image_filename(instance, filename):
    name = instance.name
    slug = slugify(name)
    return f"products/{slug}-{filename}"


class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(ProductTag, blank=True)
    desc = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to=get_image_filename, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = generate_slug(self.name)
        super(Product, self).save(*args, **kwargs)


class Price(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name = "price")
    price = models.DecimalField(decimal_places=2, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product.name} {self.price}"
