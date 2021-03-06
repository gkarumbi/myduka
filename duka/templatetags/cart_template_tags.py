from django import template 
from duka.models import Order

register = template.Library()

@register.filter 
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user , ordered = False)
        if qs.exists():
            return qs[0].items.count()
        
        else:

     
            return 0
    else:
        return 0


