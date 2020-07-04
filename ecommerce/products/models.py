from django.db import models

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
    bottom_price = models.IntegerField( blank=True)


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