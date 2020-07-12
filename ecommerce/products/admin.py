from django.contrib import admin
from products.models import Category, Product, CIM, Item, Order,OIM, Cart, Comment
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CIM)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OIM)
admin.site.register(Comment)
# admin.site.register(ProductImage)
