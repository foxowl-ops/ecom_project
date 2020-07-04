from django.contrib import admin
from products.models import Category, Product, Option, Size
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Option)
# admin.site.register(ProductImage)
