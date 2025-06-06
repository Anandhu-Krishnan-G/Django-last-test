from django.shortcuts import render,redirect ,get_object_or_404
from store.models import Product
from .models import Cart
from .models import CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        # request.session.create()
        cart=request.session.create()

    return cart


def add_cart(request,product_id):
    color=request.GET['color']
    # size=request.GET['size']
    return HttpResponse(color)
    exit()
    product=Product.objects.get(id=product_id)  #get produtc
    try:
        #cart=Cart.objects.get(cart_id=_cart_id)
        #cart=Cart.objects.get(cart_id=_cart_id(request)) get the cart using cart_id present in the session
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if not cart:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item=CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )

        cart_item.save()
        print(cart_item.quantity)
        print(cart_item.product)
    return redirect('cart')


def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')



def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=tax+total
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total

    }

    return render(request,'store/cart.html',context)