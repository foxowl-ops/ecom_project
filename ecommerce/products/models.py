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
    stock = models.IntegerField()
    original_price = models.IntegerField( blank=True)
    discounted_price = models.IntegerField(blank=True)

    def __str__(self):
        return self.name


# class ProductImage(models.Model):
#     image = models.ImageField(upload_to="products/", blank = True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.product)

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    product = models.ForeignKey(Product,blank=True ,on_delete=models.CASCADE)
    size = models.CharField(max_length=100)
    quantity = models.IntegerField(blank=True)

    def get_price(self, *args, **kwargs):
        return self.product

class CIM(models.Model):
    cart = models.ForeignKey(Cart,blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,blank=True, on_delete=models.CASCADE)

class Order(models.Model):
    statuses = [("O","Ordered"), ("S","Shipped"),("C","Cancelled"),("D","Delivered"),("R","Returned"),("L","Lost")]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    shipment_date = models.DateTimeField(auto_now_add=False, blank=True)
    status = models.CharField(max_length=1, choices=statuses, default = "O" )

class OIM(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

