from django.shortcuts import render,get_object_or_404,redirect
from .models import Categories,Product,Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect

from .forms import CreateUserForm
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

def products(request,slug):
    product = get_object_or_404(Product, product_slug=slug)

    return render(request, 'product_page.html',{'product':product})


@login_required(login_url ='login')
def shoppingcart(request):
    try:
        order = Order.objects.get(user= request.user, ordered= False)
        context ={
            "object": order
        }
    except ObjectDoesNotExist:
        messages.error(self.request, "You do not have an active order")
        return redirect("/")


    return render(request,'shopping_cart.html', context)



@login_required(login_url ='login')
def checkout(request):


    return render(request,'checkout.html')




@csrf_exempt
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username =request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.info(request, "Username OR Password is incorrect")
                return render(request, 'accounts/login.html')


        return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect ('login')


@csrf_exempt
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"Account was created for " + user)
                return redirect('login')


        context ={'form':form}
        return render(request, 'accounts/register.html', context)

@login_required
def add_to_cart(request,slug):
    product = get_object_or_404(Product, product_slug =slug)
    order_item,created = OrderItem.objects.get_or_create(item =product, user =request.user,ordered=False)
    order_qs = Order.objects.filter(user =request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__product_slug = product.product_slug).exists():
            
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"This item quantitiy was updated")
        else:
            messages.info(request,"This item was added to your cart ")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item quantitiy was updated")

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



def remove_from_cart(request,slug):
    product = get_object_or_404(Product, product_slug =slug)
    order_qs = Order.objects.filter(user =request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__product_slug = product.product_slug).exists():
            order_item = OrderItem.objects.filter(
                item =product, 
                user =request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item quantitiy was removed from your cart")
        else:
            messages.info(request,"This item quantitiy was not in your cart")
            return redirect("products", slug=slug)
    
    else:
        messages.info(request,"You do not have an active order  was updated")
        return redirect("products", slug=slug)

    return redirect("products", slug=slug)


def remove_single_item_from_cart(request,slug):
    product = get_object_or_404(Product, product_slug =slug)
    order_qs = Order.objects.filter(user =request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__product_slug = product.product_slug).exists():
            order_item = OrderItem.objects.filter(
                item =product, 
                user =request.user,
                ordered=False
            )[0]
            if order_item.quantitiy>1:
                order_item.quantitiy -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                
                messages.info(request,"This item quantitiy was removed from your cart")
                return redirect("shoppingcart", slug=slug)
        else:
            messages.info(request,"This item quantitiy was not in your cart")
            print(slug)
            
            return redirect("products", slug=slug)
    
    else:
        
        messages.info(request,"You do not have an active order  was updated")
        return redirect("products", slug=slug)

     

        