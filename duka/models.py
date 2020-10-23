from django.db import models

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length =100)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_brand = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/products', blank=True, null=True)
    product_description = models.TextField(blank=True)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE,blank=True)


    def __str__(self):
        return self.product_name