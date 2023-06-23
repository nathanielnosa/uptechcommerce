from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from . models import *
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages
from . forms import CheckoutForm
from django.conf import settings
# Create your views here.

def index(request):
    # sliders
    sliders = Slider.objects.all()
    # category
    category = Category.objects.all().order_by('-created_at')[:4]
    # product
    products = Product.objects.all().order_by('-created_at')[:3]

    context={
        'sliders':sliders,
        'categorys': category,
        'products': products,
    }

    return render(request, 'stores/index.html',context)

# all products 
def stores(request):
    products = Product.objects.all().order_by('-created_at')
    # paginator
    paginator = Paginator(products,4)
    page_number = request.GET.get("page")
    page_list = paginator.get_page(page_number)

    context={
        'products':products,
        'paginator':page_list
    }
    return render(request, 'stores/stores.html',context)

# single prouct
def store(request,id):
    product = Product.objects.get(id=id)
    context={
        'product':product
    }
    return render(request, 'stores/store.html',context)

# category
def category(request,id):
    category = Product.objects.all().filter(category = id)
    context={
        'category':category
    }
    return render(request, 'stores/category.html',context)

# search
def search(request):
    getKword = request.GET.get('kword')

    product = Product.objects.filter(Q(title__icontains = getKword) | Q(description__icontains = getKword) | Q(price__lte = getKword))

    context = {
        'product': product
    }
    return render(request, 'stores/search.html',context)


# add to cart
def addtocart(request,id):
    # get the product
    cart_product = Product.objects.get(id=id)

    # check if there is in cart
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart_item = get_object_or_404(Cart, id=cart_id)

        # check or assign cart to a registered user
        if request.user.is_authenticated and request.user.profile:
            cart_item.profile = request.user.profile
            cart_item.save()

        # check if there is in existing product in cart
        this_product_in_cart = cart_item.cartproduct_set.filter(product = cart_product) 
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += cart_product.price
            cartproduct.save()
            cart_item.total += cart_product.price
            cart_item.save()
            messages.success(request,'item increase in cart')

        else:
            cartproduct = CartProduct.objects.create(cart = cart_item, product= cart_product, quantity =1, subtotal= cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()
            messages.success(request,'item added to cart')


    else:
        cart_item = Cart.objects.create(total =0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(cart = cart_item, product= cart_product, quantity =1, subtotal= cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()
        messages.success(request,'item added to cart')

    
    return redirect('index')

# my cart
def myCart(request):
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart_item = Cart.objects.get(id = cart_id)
        # check or assign cart to a registered user
        if request.user.is_authenticated and request.user.profile:
            cart_item.profile = request.user.profile
            cart_item.save()
    else:
        cart_item = None
    
    context={
        'cart': cart_item
    }
    return render(request, 'stores/mycart.html',context)

    
# manage cart
def manageCart(request,id):
    # get the cart
    cart_obj = CartProduct.objects.get(id=id) #cart,product,qty,sub
    cart = cart_obj.cart

    # get the clicked action
    action = request.GET.get('action')

    if(action == 'inc'):
        cart_obj.quantity += 1
        cart_obj.subtotal +=cart_obj.product.price
        cart_obj.save()
        cart.total+=cart_obj.product.price
        cart.save()
        messages.success(request,'item increase in cart')

    elif(action == 'dcr'):
        cart_obj.quantity -= 1
        cart_obj.subtotal -=cart_obj.product.price
        cart_obj.save()
        cart.total-=cart_obj.product.price
        cart.save()
        if(cart_obj.quantity == 0):
            cart_obj.delete()
            cart.save()
        messages.success(request,'item decrease in cart')
    elif(action == 'rmv'):
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()

    return redirect('myCart')


def checkout(request):
    cart_id = request.session.get('cart_id',None)
    cart_item = Cart.objects.get(id = cart_id)
    
    form = CheckoutForm()
    
    # check authentication and authorization
    if request.user.is_authenticated and request.user.profile:
        pass
    else:
        return redirect('/user/login/?next=/checkout/')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.cart = cart_item
            form.amount = cart_item.total
            form.subtotal = cart_item.total
            form.discount = 0
            paymentmethod = form.payment_method
            del request.session['cart_id']
            form.save()

            order = form.id
            if paymentmethod == 'paystack':
                return redirect('payment', id = order)

    context={
        'form':form,
        'cart':cart_item
    }
    return render(request, 'stores/checkout.html',context)

def payment(request,id):
    orders  =  Order.objects.get(id=id)
    context={
        'order':orders,
        'paystack':settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'stores/payment.html',context)

def verify_payment(request:HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Order, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request,'verification successful')
    else:
        messages.success(request,'verification failed')
    return redirect('dashboard')

    