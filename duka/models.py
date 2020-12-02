from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class Categories(models.Model):
    category_name = models.CharField(max_length =100)
    category_slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("categories", kwargs={"slug":self.category_slug})

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/products', blank=True, null=True)
    product_description = models.TextField(blank=True)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE,blank=True)
    product_slug = models.SlugField()


    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("products", kwargs={"slug":self.product_slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"slug":self.product_slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"slug":self.product_slug})


    @classmethod
    def get_product_brand(cls,self):
        products = cls.objects.filter(product_category=self.id)
        for product in products:
            print(product.product_brand)
            return self.product_brand


    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ""
        return url



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=True)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.product_price

    def get_total_order(self):
        return self.get_total_item_price

class Order(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total_order_value(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()

        return total 