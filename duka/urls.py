from django.conf.urls import url
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns =[
    url(r'^$', views.home, name = 'home'),
    url(r'^categories/(?P<slug>[-\w]+)$', views.categories, name='categories'),
    url(r'^products/(?P<slug>[-\w]+)$', views.products, name='products'),
    url(r'^shoppingcart/', views.shoppingcart, name='shoppingcart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^register/$', views.registerUser, name='register'),
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^add-to-cart/(?P<slug>[-\w]+)$', views.add_to_cart, name='add-to-cart'),
    url(r'^remove-from-cart/(?P<slug>[-\w]+)$', views.remove_from_cart, name='remove-from-cart'),
    #url(r'^remove-single-item-from-cart/(?P<slug>[-\w]+)$', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('remove-item-from-cart/<slug:slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)