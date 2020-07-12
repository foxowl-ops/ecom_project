from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
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
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    def save(self, *args, **kwargs):
        discount = self.product.discounted_price
        qty = self.quantity
        self.total = int(discount)*int(qty)
        print(self.total)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name


class CIM(models.Model):
    cart = models.ForeignKey(Cart,blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,blank=True, on_delete=models.CASCADE)
    total = models.IntegerField(null=True)
    def save(self, *args, **kwargs):
        self.total = int(self.item.product.discounted_price) * int(self.item.quantity)
        super(CIM,self).save(*args, **kwargs)

class Order(models.Model):
    statuses = [("O","Ordered"), ("S","Shipped"),("C","Cancelled"),("D","Delivered"),("R","Returned"),("L","Lost")]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    shipment_date = models.DateTimeField(auto_now_add=False, null=True)
    status = models.CharField(max_length=1, choices=statuses, default = "O" )
    total_bill = models.IntegerField()

    def save(self,*args, **kwargs):
        if self.shipment_date is None:
            self.shipment_date = datetime.now() + timedelta(days=7)
        super(Order, self).save(*args, **kwargs)

class OIM(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject