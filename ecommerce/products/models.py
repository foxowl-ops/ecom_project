from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category= models.ForeignKey(Category, on_delete= models.CASCADE)
    discount= models.FloatField()
    image = models.ImageField()

    def get_product_price_small(self,*args, **kwargs):
        return self.option_set.all()[0].unit_price
    def get_product_price_big(self,*args, **kwargs):
        return self.option_set.all()[1].unit_price

    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size

class Option(models.Model):
    bottle_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    unit_price = models.IntegerField( blank=True)

    def __str__(self):
        return self.product.name

# class ProductImage(models.Model):
#     image = models.ImageField(upload_to="products/", blank = True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.product)

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

class Item(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class CIM(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

class Order(models.Model):
    statuses = [("O","Ordered"), ("S","Shipped"),("C","Cancelled"),("D","Delivered"),("R","Returned"),("L","Lost")]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    shipment_date = models.DateTimeField(auto_now_add=False, blank=True)
    status = models.CharField(max_length=1, choices=statuses, default = "O" )

class OIM(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

