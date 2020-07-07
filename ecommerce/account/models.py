from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    contact_no = PhoneNumberField()
    address1 = models.TextField()
    address2 = models.TextField()

    REQUIRED_FIELDS=['email','contact_no']

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("detailuser", args = [self.id])

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Item(models.Model):
#     product = 