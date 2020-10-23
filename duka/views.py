from django.shortcuts import render
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


def categories(request,cat):
    category = Categories.objects.filter(name=cat)
    print(category)

    return render(request,'category.html',{'category':category})