from django.db import models
from django.urls import reverse
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


    def __str__(self):
        return self.product_name

    @classmethod
    def get_product_brand(cls,self):
        products = cls.objects.filter(product_category=self.id)
        for product in products:
            print(product.product_brand)
            return self.product_brand