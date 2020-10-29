from django.shortcuts import render,get_object_or_404
from .models import Categories,Product

# Create your views here.

def home(request):
    """
    Retriieve all category objects for displaying on our category panel
    """
    categories = Categories.objects.all()
    products = Product.objects.all()
    print(products)

    return render(request, 'index.html', {'categories':categories,'products':products})


def categories(request,slug):
    """ category = Categories.objects.get(category_slug=slug)
    print(category) """
    category = get_object_or_404(Categories,category_slug=slug)
    products = Product.objects.filter(product_category=category.pk)
    for product in products:
        print(product.product_brand)
        
    #print(get_product_brand())

    return render(request,'category.html',{'products':products, "category":category})